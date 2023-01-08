import pygame
import random
import os
import sys
import res

from pygame.locals import *

# 초기화
pygame.init()
pygame.mixer.init()

# 라이브러리
this_path = os.path.dirname(sys.argv[0])

# 기본 설정 (수정 금지)
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_icon(pygame.image.load(res.entity["poop"]))
pygame.display.set_caption("Avoid!")
clock = pygame.time.Clock()

# 기본 배경
background = pygame.image.load(res.background["default"][0])
setting_font = pygame.font.Font(res.font["NeoDunggeunmo"], 22)

class s_root():
    def __init__(self):
        self.main = None
        self.selection:list = None
        self.color = (255, 255, 255)
        self.text_render = setting_font.render(str(self.main), True, self.color)
        self.selected = False

    def reload(self, main=None, selection=None, text_render=None):
        self.main = main
        self.selection = selection
        self.text_render = text_render

    def isSelect(self):
        if self.selected:
            self.color = (86, 255, 86)
        else:
            self.color = (255, 255, 255)
        self.text_render = setting_font.render(str(self.main), True, self.color)

# 기본 설정
class s_mode(s_root):
    def __init__(self):
        super().__init__()
        self.main = "Normal"                 # 모드(추가 예정)
        self.selection = ["Normal", "Poison", "Radiation", "MIXED"]
        self.text_render = setting_font.render(str(self.main), True, self.color)

class s_difficulty(s_root):
    def __init__(self):
        super().__init__()
        self.main = 2              # 난이도 
        self.selection = [2, 3, 4, 1]
        self.text_render = setting_font.render(str(self.main), True, self.color)

class s_player_type(s_root):
    def __init__(self):
        super().__init__()
        self.main = "Single"      # 플레이어 모드
        self.selection = ["Single", "Multi"]
        self.text_render = setting_font.render(str(self.main), True, self.color)

class s_score_type(s_root):
    def __init__(self):
        super().__init__()
        self.main = "Difficulty"   # 점수 환산 방식
        self.selection = ["Difficulty", "Count"]
        self.text_render = setting_font.render(str(self.main), True, self.color)

class s_use_sound(s_root):
    def __init__(self):
        super().__init__()
        self.main = True            # 브금 여부
        self.selection = [True, False]
        self.text_render = setting_font.render(str(self.main), True, self.color)

class s_theme(s_root):
    def __init__(self):
        super().__init__()
        self.main = "LIGHT"              # 테마 
        self.selection = ["LIGHT", "DARK"]
        self.text_render = setting_font.render(str(self.main), True, self.color)

class s_solid_background(s_root):
    def __init__(self):
        super().__init__()
        self.main = False    # 단색 배경 사용
        self.selection = [False, True]
        self.text_render = setting_font.render(str(self.main), True, self.color)

class s_show_fps(s_root):
    def __init__(self):
        super().__init__()
        self.main = True             # fps 표시 여부
        self.selection = [True, False]
        self.text_render = setting_font.render(str(self.main), True, self.color)

class s_fps_set(s_root):
    def __init__(self):
        super().__init__()
        self.main = 144                # fps 설정
        self.selection = [30, 60, 144, 10, 20]
        self.text_render = setting_font.render(str(self.main), True, self.color)

class s_language(s_root):
    def __init__(self):
        super().__init__()
        self.main = "En-US"
        self.selection = ["En-US", "Ko-KR"]
        self.text_render = setting_font.render(str(self.main), True, self.color)

selectS_s = [
    # in-game
    s_mode(), s_difficulty(), s_player_type(), s_score_type(),
    # preference
    s_use_sound(), s_theme(), s_solid_background(), s_show_fps(), s_fps_set(), s_language()
]

selectS = 0

# 엔티티
class Entity():
    def __init__(self, image: str, scale: float):
        self.image:pygame.Surface = pygame.image.load(image)
        self.image_str:str = image
        self.before_size: list = self.image.get_rect().size
        self.scale: tuple(float, float) = (self.before_size[0] * scale, self.before_size[1] * scale)
        self.image = pygame.transform.scale(self.image, self.scale)
        self.image_o = pygame.transform.scale(self.image, self.scale)
        self.size:list = self.image.get_rect().size          
        self.width:float = self.size[0]                     
        self.height:float = self.size[1]
        self.x:float = 0
        self.y:float = 0                                         
        self.speed:float = 0                                     
        self.rect:Rect = None

    # 충돌 감지 비교 요소
    def setRect(self):
        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y

    # 그리기
    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    # 숨기기
    def hideEntity(self):
        self.image = pygame.image.load(res.empty_image)

    # 보이기
    def showEntity(self):
        self.image = self.image_o

# 플레이어
class Player(Entity):
    def __init__(self, image):
        super().__init__(image, 0.6)
        self.x = (screen_width / 2) - (self.width / 2)         
        self.y = float(screen_height) - self.height             # 플레이어 y좌표
        self.to_x = 0                                       # 플레이어 이동할 x좌표
        self.speed = 0.2                                    # 플레이어 속도
        self.score = 0                                      # 플레이어 점수
        self.health = 100                                   # 플레이어 체력
    # 화면 밖 나가기 제한
    def limitPos(self):
        if self.x < 0:
            self.x = 0
        elif self.x > screen_width - self.width:
            self.x = screen_width - self.width
    
    # 이동
    def move(self, frame):
        self.x += frame * self.to_x

    # 체력 피해
    def giveDamage(self, damage):
        self.health -= damage
        game_font = pygame.font.Font(res.font["NeoDunggeunmo"], 20)
        gotDamage = game_font.render("-" + str(damage), True, (255, 0, 0))
        screen.blit(gotDamage, (self.x + 15, self.y - 15))
        if self.health <= 0:
            self.health = 0
    
    # 체력 획득
    def giveHeal(self, health):
        self.health += health
        game_font = pygame.font.Font(res.font["NeoDunggeunmo"], 20)
        gotHeal = game_font.render("+" + str(health), True, (0, 255, 0))
        screen.blit(gotHeal, (self.x + 15, self.y - 15))
        if self.health >= 100:
            self.health = 100
    
    # 초기화
    def reset(self):
        self.x = (screen_width / 2) - (self.width / 2)
        self.y = screen_height - self.height
        self.speed = 0.3
        self.score = 0   
        self.health = 100
        self.to_x = 0          

    # 피해 레벨 (0 ~ 3)
    def checkLevel(self):
        if 70 < self.health:
            return 0
        elif 50 < self.health <= 70:
            return 1
        elif 20 < self.health <= 50:
            return 2
        elif 0 < self.health <= 20:
            return 3
        else:
            return 4

    # 죽었는지 확인
    def isDie(self):
        if self.checkLevel() == 4:
            return True
        else:
            return False
    
# 똥
class Poop(Entity):
    def __init__(self, image):
        super().__init__(image, 0.8)
        self.x = random.randint(0, screen_width - int(round(self.width)))
        self.y = 0 - self.height
        self.speed = (random.randint(1, 4)) / 10
        self.rect = None
        if selectS_s[0].main == "MIXED":
            if self.image_str == PoopImage[0]:
                self.damage = PoopDamage[0]
            elif self.image_str == PoopImage[1]:
                self.damage = PoopDamage[1]
            elif self.image_str == PoopImage[2]:
                self.damage = PoopDamage[2]
        else:
            self.damage = PoopDamage

    # 소멸되었을 때
    def isDestroy(self):
        return self.y > screen_height

    # 이동
    def move(self, frame):
        self.y += frame * self.speed

    # 초기화
    def reset(self):
        self.y = 0 - self.height

# 아이템
class Item(Entity):
    def __init__(self, image):
        super().__init__(image, 0.8)
        self.isLand:bool = False
        self.onLandTime:int = 0
        self.nowTime:int = 0
        self.destroyTime:int = 10

    # 초기화
    def reset(self):
        self.y = 0 - self.height
        self.isLand = False

    # 랜딩했을 때, 소멸되었는가
    def isOnLand(self, frame):
        if self.isLand:
            if self.onLandTime == 0:
                self.onLandTime = pygame.time.get_ticks()
                return True

            elif self.onLandTime != 0:
                self.nowTime = pygame.time.get_ticks()
                return self.isDestroy(frame)
        return True

    # 소멸 조건
    def isDestroy(self, frame):
        return self.nowTime - self.onLandTime < self.destroyTime * frame

    # 이동
    def move(self, frame):
        if not self.isLand:
            self.y += frame * self.speed
            if self.y >= screen_height - self.height:
                self.y = screen_height - self.height
                self.isLand = True

# 긴급 킷
class AidKit(Item):
    def __init__(self, image):
        super().__init__(image)
        self.x = random.randint(0, screen_width - int(round(self.width)))
        self.y = 0 - self.height
        self.speed = (random.randint(1, 4)) / 10
        self.heal = 5

# 음악 재생
class Sound:
    def __init__(self):
        self.soundtrack = res.sound["rollin_at_5"]
        self.isStart = False
        self.isToned = False
        self.theme = selectS_s[5].main
        self.load = pygame.mixer.music.load(self.soundtrack[0])

    def setMusicTheme(self):
        if selectS_s[5].main == "LIGHT":
            self.theme = selectS_s[5].main
            self.soundtrack = res.sound["rollin_at_5"]
            self.load = pygame.mixer.music.load(self.soundtrack[0])
        elif selectS_s[5].main == "DARK":
            self.theme = selectS_s[5].main
            self.soundtrack = res.sound["raving_energy"]
            self.load = pygame.mixer.music.load(self.soundtrack[0])

    def play(self):
        if selectS_s[4].main:
            pygame.mixer.music.play(1000, 0.0)
            self.isStart = True

    def stop(self):
        if selectS_s[4].main:
            pygame.mixer.music.stop()
            self.isStart = False

    def toneUp(self):
        self.load = pygame.mixer.music.load(self.soundtrack[1])
        self.isToned = True

    def reset(self):
        self.load = pygame.mixer.music.load(self.soundtrack[0])
        self.isStart = False
        self.isToned = False

PoopList = []   # 똥 인스턴스 생성 목록
PoopCount = 0   # 똥 갯수
PoopImage = res.entity["poop"]
PoopDamage = 30
ItemList = []   # 아이템 인스턴스 생성 목록
ItemCount = 0   # 아이템 갯수

def loadBackground(backType, filter=None) -> list:
    returnValue = []
    if selectS_s[5].main == "LIGHT":
        if selectS_s[6].main:
            returnValue.append(pygame.image.load(res.background["solid"][0]))
        else:
            returnValue.append(pygame.image.load(backType[0]))
    elif selectS_s[5].main == "DARK":
        if selectS_s[6].main:
            returnValue.append(pygame.image.load(res.background["solid"][1]))
        else:
            returnValue.append(pygame.image.load(backType[1]))

    if filter != None:
        if selectS_s[9].main == "En-US":
            returnValue.append(pygame.image.load(filter[0]))
        elif selectS_s[9].main == "Ko-KR":
            returnValue.append(pygame.image.load(filter[1]))
    
    return tuple(returnValue)
    
# 만약 게임오버라면,
isGameOver = False

# 구역
areaList = ["title", "setting", "info", "start", "end"]    # 구역 목록
area = areaList[0]                      # 현재 구역

# 인스턴스
player = Player(res.entity["sprite"])                       # 플레이어 메인 인스턴스
player2 = Player(res.entity["sprite2"])
sound = Sound()                         # 배경 음악

selectS_s[0].selected = True
selectS_s[0].isSelect()

# 이벤트 루프
running = True
while running:
    dt = clock.tick(selectS_s[8].main)                                                        # fps 설정
    fps = clock.get_fps()                                                           # fps 구하기
    fontfps = pygame.font.Font(res.font["NeoDunggeunmo"], 20)
    if (selectS_s[7]).main:
        fpscounter = fontfps.render(f"{int(fps)}fps", True, (255, 255, 255))        # fps 화면에 렌더링
    else:
        fpscounter = fontfps.render("", True, (255, 255, 255))

    # 이벤트 관리
    for event in pygame.event.get():
        # 만약 X버튼을 눌렀을때
        if event.type == pygame.QUIT:
            running = False

        # 만약 구역이 title 이라면
        if area == areaList[0]:
            if event.type == pygame.KEYDOWN:    # 키를 눌렀을때
                if event.key == pygame.K_SPACE:
                    area = areaList[3]
                    PoopCount = selectS_s[1].main * 3
                    ItemCount = selectS_s[1].main
                    
                    if selectS_s[0].main == "Normal":
                        PoopImage = res.entity["poop"]
                        PoopDamage = 30
                    elif selectS_s[0].main == "Poison":
                        PoopImage = res.entity["poop2"]
                        PoopDamage = 70
                    elif selectS_s[0].main == "Radiation":
                        PoopImage = res.entity["poop3"]
                        PoopDamage = 100
                    elif selectS_s[0].main == "MIXED":
                        PoopImage = [res.entity["poop"], res.entity["poop2"], res.entity["poop3"]]
                        PoopDamage = [30, 70, 100]

                    if selectS_s[0].main != "MIXED":
                        for i in range(PoopCount):      # 난이도 만큼 인스턴스 생성
                            PoopList.append(Poop(PoopImage))
                    else:
                        for i in range(PoopCount):
                            if i <= PoopCount / 3:
                                PoopList.append(Poop(PoopImage[0]))
                            elif PoopCount / 3 < i <= PoopCount / 3 * 2:
                                PoopList.append(Poop(PoopImage[1]))
                            elif PoopCount / 3 * 2 < i <= PoopCount:
                                PoopList.append(Poop(PoopImage[2]))

                    for i in range(ItemCount):      # 난이도 만큼 인스턴스 생성
                        ItemList.append(AidKit(res.item["aidkit"]))

                    pygame.display.update()
                elif event.key == pygame.K_LCTRL:
                    area = areaList[1]
                    pygame.display.update()
                elif event.key == pygame.K_LALT:
                    area = areaList[2]
                    pygame.display.update()

        # 만약 구역이 setting 이라면
        elif area == areaList[1]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    area = areaList[0]
                    selectS = 0
                    for index, i in enumerate(selectS_s):
                        selectS_s[index].selected = False
                        selectS_s[index].isSelect()

                    selectS_s[0].selected = True
                    selectS_s[0].isSelect()
                    pygame.display.update()

                elif event.key == pygame.K_TAB:
                    selectS += 1
                    if selectS > len(selectS_s) - 1:
                        selectS = 0
                        selectS_s[selectS].selected = True
                        selectS_s[selectS].isSelect()
                        selectS_s[len(selectS_s) - 1].selected = False
                        selectS_s[len(selectS_s) - 1].isSelect()
                    else:
                        selectS_s[selectS].selected = True
                        selectS_s[selectS].isSelect()
                        selectS_s[selectS - 1].selected = False
                        selectS_s[selectS - 1].isSelect()

                    # 선택 커서 구현 필요
                elif event.key == pygame.K_LALT:
                    selectS_s[selectS].main = selectS_s[selectS].selection[1]
                    to_push_back = selectS_s[selectS].selection[0]
                    selectS_s[selectS].selection.append(to_push_back)
                    del selectS_s[selectS].selection[0]
                    break

        # 만약 구역이 info 이라면
        elif area == areaList[2]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    area = areaList[0]
                    pygame.display.update()

        # 만약 구역이 start 이라면
        elif area == areaList[3]:                    
            if event.type == pygame.KEYDOWN:    # 키가 눌렸을때
                if not player.isDie():
                    if event.key == pygame.K_a:            # a는 왼쪽, d는 오른쪽으로 이동
                        player.to_x -= player.speed
                    if event.key == pygame.K_d:
                        player.to_x += player.speed
                if not player2.isDie():
                    if event.key == pygame.K_LEFT:            # <-는 왼쪽, ->는 오른쪽으로 이동
                        player2.to_x -= player.speed
                    if event.key == pygame.K_RIGHT:
                        player2.to_x += player.speed

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    player.to_x = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player2.to_x = 0
                

        # 만약 구역이 end 이라면
        elif area == areaList[4]:
            if event.type == pygame.KEYDOWN:    # 키가 눌렸을 때
                if event.key == pygame.K_SPACE:        # 스페이스 바를 눌렀을 때, 초기화 및 초기 화면
                    area = areaList[0]
                    isGameOver = False
                    player.reset()
                    player2.reset()
                    PoopCount = 0
                    PoopList = []
                    ItemCount = 0
                    ItemList = []
                    pygame.display.update()

    # title 구역
    if area == areaList[0]:
        sound.setMusicTheme()
        background, background_filter = loadBackground(res.background["darken"], res.background["filter"]["on_title"])  # 블러된 배경화면 로딩

        screen.blit(background, (0, 0))
        screen.blit(background_filter, (0, 0))
        screen.blit(fpscounter, (screen_width - 65, 5))

    # setting 구역
    elif area == areaList[1]:
        for index, i in enumerate(selectS_s):
            selectS_s[index].isSelect()

        background, background_filter = loadBackground(res.background["darken"], res.background["filter"]["on_setting"])
        game_font = pygame.font.Font(res.font["NeoDunggeunmo"], 17)

        screen.blit(background, (0, 0))
        screen.blit(background_filter, (0, 0))
        screen.blit(fpscounter, (screen_width - 65, 5))
        screen.blit(selectS_s[0].text_render, (screen_width / 4 - 25, screen_height / 2 + -15)) # 20 간격
        screen.blit(selectS_s[1].text_render, (screen_width / 4 + 25, screen_height / 2 + 10))
        screen.blit(selectS_s[2].text_render, (screen_width / 4 - 5, screen_height / 2 + 30))
        screen.blit(selectS_s[3].text_render, (screen_width / 4 + 45, screen_height / 2 + 50))
        screen.blit(selectS_s[4].text_render, (screen_width / 2 + 150, screen_height / 2 + -15))
        screen.blit(selectS_s[5].text_render, (screen_width / 4 + 5, screen_height / 2 + 100))
        screen.blit(selectS_s[6].text_render, (screen_width / 4 - 10, screen_height / 2 + 120))
        screen.blit(selectS_s[7].text_render, (screen_width / 2 + 150, screen_height / 2 + 5))
        screen.blit(selectS_s[8].text_render, (screen_width / 2 + 150, screen_height / 2 + 25))
        screen.blit(selectS_s[9].text_render, (screen_width / 2 + 150, screen_height / 2 + 45))

    # info 구역
    elif area == areaList[2]:
        background, background_filter = loadBackground(res.background["darken"], res.background["filter"]["on_info"])
        screen.blit(background, (0, 0))
        screen.blit(background_filter, (0, 0))
        screen.blit(fpscounter, (screen_width - 65, 5))
        
    # start 구역
    elif area == areaList[3]:
        if not sound.isStart:
            sound.play()
        
        background = loadBackground(res.background["default"])[0]       # 배경화면 로딩
        screen.blit(background, (0, 0))

        if selectS_s[2].main == "Single":
            if player.checkLevel() < 3 and sound.isToned:
                sound.stop()
                sound.reset()
                sound.play()

            if player.checkLevel() == 3 and not sound.isToned:
                sound.stop()
                sound.toneUp()
                sound.play()

        elif selectS_s[2].main == "Multi":
            if (player.checkLevel() < 3 or player.isDie()) and (player2.checkLevel() < 3 or player2.isDie()) and sound.isToned:
                sound.stop()
                sound.reset()
                sound.play()

            if (player.checkLevel() == 3 or player2.checkLevel() == 3) and not sound.isToned:
                sound.stop()
                sound.toneUp()
                sound.play()

            player2.move(dt)
            player2.limitPos()
            player2.setRect()
            player2.draw()

        player.move(dt)     # 프레임을 인자로 해서 이동
        player.limitPos()   # 제한되는 지 확인
        player.setRect()    # rect 설정하기
        player.draw()       # 출력

        isDeleted = False
        for index, ItemInst in enumerate(ItemList):
            ItemInst.move(dt)
            ItemInst.setRect()
            if player.rect.colliderect(ItemInst.rect) and not player.isDie():
                player.giveHeal(ItemInst.heal)
                del ItemList[index]
                isDeleted = True
            if selectS_s[2].main == "Multi":
                if player2.rect.colliderect(ItemInst.rect) and not player2.isDie():
                    player2.giveHeal(ItemInst.heal)
                    if not isDeleted:
                        del ItemList[index]
                        isDeleted = True

            if isDeleted:
                continue

            if not ItemInst.isOnLand(dt):
                del ItemList[index]
            ItemInst.draw()
            isDeleted = False

        isDeleted = False
        delObj = []
        for index, PoopInst in enumerate(PoopList):
            PoopInst.move(dt)
            PoopInst.setRect()
            if player.rect.colliderect(PoopInst.rect) and not player.isDie():  # 충돌 감지
                player.giveDamage(PoopInst.damage)
                delObj.append(PoopList[index])
                del PoopList[index]
                isDeleted = True
            if selectS_s[2].main == "Multi" and not player2.isDie():
                if player2.rect.colliderect(PoopInst.rect):
                    player2.giveDamage(PoopInst.damage)
                    if not isDeleted:
                        delObj.append(PoopList[index])
                        del PoopList[index]
                        isDeleted = True
            if PoopInst.isDestroy():    # 소멸 감지
                delObj.append(PoopList[index])
                del PoopList[index]
                if selectS_s[3].main == "Difficulty":
                    if not player.isDie():
                        player.score += 1 / selectS_s[1].main
                    if selectS_s[2].main == "Multi" and not player2.isDie():
                        player2.score += 1 / selectS_s[1].main
                else:
                    player.score += 1
                    if selectS_s[2].main == "Multi" and not player2.isDie():
                        player2.score += 1

            isDeleted = False
        
        if player.isDie():
            player.hideEntity()
        else:
            player.showEntity()
        
        if selectS_s[2].main == "Multi":
            if player2.isDie():
                player2.hideEntity()
            else:
                player2.showEntity()

        isGameOver = player.isDie()
        if selectS_s[2].main == "Multi":
            isGameOver = player.isDie() and player2.isDie()

        for PoopInst in PoopList:
            if isGameOver:
                PoopInst.reset()
            PoopInst.draw() # 출력
        
        for ItemInst in ItemList:
            if isGameOver:
                ItemInst.reset()
            ItemInst.draw() # 출력

        if isGameOver:      # 게임 오버시
            area = areaList[4]  # 게임 오버 화면으로 이동
            pygame.display.update()

        if len(ItemList) != ItemCount: 
            for i in range(ItemCount - len(ItemList)):
                ItemList.append(AidKit(res.item["aidkit"]))

        if len(PoopList) != PoopCount:
            for i in range(PoopCount - len(PoopList)):  
                if selectS_s[0].main != "MIXED":
                    PoopList.append(Poop(PoopImage))
                else:
                    if delObj[i].image_str == PoopImage[0]:
                        PoopList.append(Poop(PoopImage[0]))
                    elif delObj[i].image_str == PoopImage[1]:
                        PoopList.append(Poop(PoopImage[1]))
                    elif delObj[i].image_str == PoopImage[2]:
                        PoopList.append(Poop(PoopImage[2]))
        
        game_font = pygame.font.Font(res.font["NeoDunggeunmo"], 30)
        scoreboard = game_font.render("P1: Score: " + str(round(player.score, 2)), True, (255, 255, 255))   # 점수를 화면에 렌더링
        screen.blit(scoreboard, (10, 10))
        healthboard = game_font.render("P1: HP: " + str(player.health), True, (255, 255, 255))   # 점수를 화면에 렌더링
        screen.blit(healthboard, (10, 35))
        if selectS_s[2].main == "Multi":
            scoreboard2 = game_font.render("P2: Score: " + str(round(player2.score, 2)), True, (255, 255, 255))   # 점수를 화면에 렌더링
            screen.blit(scoreboard2, (screen_width / 2 + 35, 10))
            healthboard2 = game_font.render("P2: HP: " + str(player2.health), True, (255, 255, 255))   # 점수를 화면에 렌더링
            screen.blit(healthboard2, (screen_width / 2 + 35, 35))
        screen.blit(fpscounter, (screen_width - 65, 5))

    # end 구역
    elif area == areaList[4]:
        sound.stop()
        sound.reset()
        background, background_filter = loadBackground(res.background["darken"], res.background["filter"]["on_end"])       # 블러 배경화면 로딩
        screen.blit(background, (0, 0))
        screen.blit(background_filter, (0, 0))
        screen.blit(fpscounter, (screen_width - 65, 5))

        player.score = round(player.score, 2)
        player2.score = round(player2.score, 2)
        game_font = pygame.font.Font(res.font["NeoDunggeunmo"], 30)
        finalScore = game_font.render("P1: Score: " + str(player.score), True, (255, 255, 255))   # 최종 점수 렌더링
        screen.blit(finalScore, (screen_width / 3, screen_height / 2 + 45))
        if selectS_s[2].main == "Multi":
            finalScore2 = game_font.render("P2: Score: " + str(player2.score), True, (255, 255, 255))   # 최종 점수 렌더링
            screen.blit(finalScore2, (screen_width / 3, screen_height / 2 + 80))
    
    # while문을 돌때 마다 각 함수와 변수를 업데이트 (pygame 시스템)
    pygame.display.update()

# while문에서 나왔을 때 바로 종료
pygame.quit()