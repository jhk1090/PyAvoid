import pygame
import os
import sys
import asset

from pygame.locals import *

# 초기화
pygame.init()
pygame.mixer.init()
from settings import settings, settings_next, settings_exit, settings_reset
import settings as SETTINGS
from entity import Player, Poop, AidKit
import entity
# 라이브러리
this_path = os.path.dirname(sys.argv[0])

# 기본 설정 (수정 금지)
screen_width = 480
screen_height = 640
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_icon(pygame.image.load(asset.entity["poop"]))
pygame.display.set_caption("Avoid!")
clock = pygame.time.Clock()

# 기본 배경
background = pygame.image.load(asset.background["default"][0])
setting_font = pygame.font.Font(asset.font["NeoDunggeunmo"], 22)

# 음악 재생
class Sound:
    def __init__(self):
        self.soundtrack = asset.sound["rollin_at_5"]
        self.isStart = False
        self.isToned = False
        self.theme = settings["background_theme"].main
        self.load = pygame.mixer.music.load(self.soundtrack[0])

    def setMusicTheme(self):
        if settings["background_theme"].main == "LIGHT":
            self.theme = settings["background_theme"].main
            self.soundtrack = asset.sound["rollin_at_5"]
            self.load = pygame.mixer.music.load(self.soundtrack[0])
        elif settings["background_theme"].main == "DARK":
            self.theme = settings["background_theme"].main
            self.soundtrack = asset.sound["raving_energy"]
            self.load = pygame.mixer.music.load(self.soundtrack[0])

    def play(self):
        if settings["use_sound"].main:
            pygame.mixer.music.play(1000, 0.0)
            if (settings["volume"].main == 0):
                pygame.mixer.music.set_volume(0)
            else:    
                pygame.mixer.music.set_volume(settings["volume"].main / 100)
            self.isStart = True

    def stop(self):
        if settings["use_sound"].main:
            pygame.mixer.music.stop()
            self.isStart = False

    def toneUp(self):
        self.load = pygame.mixer.music.load(self.soundtrack[1])
        self.isToned = True

    def reset(self):
        self.load = pygame.mixer.music.load(self.soundtrack[0])
        self.isStart = False
        self.isToned = False

def loadBackground(backType, filter=None) -> list:
    returnValue = []
    if settings["background_theme"].main == "LIGHT":
        if settings["background_solid"].main:
            returnValue.append(pygame.image.load(asset.background["solid"][0]))
        else:
            returnValue.append(pygame.image.load(backType[0]))
    elif settings["background_theme"].main == "DARK":
        if settings["background_solid"].main:
            returnValue.append(pygame.image.load(asset.background["solid"][1]))
        else:
            returnValue.append(pygame.image.load(backType[1]))

    if filter != None:
        if settings["language"].main == "En-US":
            returnValue.append(pygame.image.load(filter[0]))
        elif settings["language"].main == "Ko-KR":
            returnValue.append(pygame.image.load(filter[1]))
    
    return tuple(returnValue)
    
# 만약 게임오버라면,
isGameOver = False

# 구역
areaList = ["title", "setting", "info", "start", "end"]    # 구역 목록
area = areaList[0]                      # 현재 구역

# 인스턴스
player = Player(asset.entity["sprite"], screen)                       # 플레이어 메인 인스턴스
player2 = Player(asset.entity["sprite2"], screen)
sound = Sound()                         # 배경 음악

settings["mode"].isSelect(True)

# 이벤트 루프
running = True

# 왼쪽으로 꾹 누르다가 오른쪽을 누르면 걸림
playerKeyInit = None # None, "A", "D"
player2KeyInit = None # None, "LEFT", "RIGHT"

while running:
    dt = clock.tick(settings["fps_set"].main)                                                        # fps 설정
    fps = clock.get_fps()                                                           # fps 구하기
    fontfps = pygame.font.Font(asset.font["NeoDunggeunmo"], 20)
    if (settings["fps_show"]).main:
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
                    entity.PoopCount = settings["difficulty"].main * 3
                    entity.ItemCount = settings["difficulty"].main
                    if settings["mode"].main == "Normal":
                        entity.PoopImage = asset.entity["poop"]
                        entity.PoopDamage = 30
                    elif settings["mode"].main == "Poison":
                        entity.PoopImage = asset.entity["poop2"]
                        entity.PoopDamage = 70
                    elif settings["mode"].main == "Radiation":
                        entity.PoopImage = asset.entity["poop3"]
                        entity.PoopDamage = 100
                    elif settings["mode"].main == "MIXED":
                        entity.PoopImage = [asset.entity["poop"], asset.entity["poop2"], asset.entity["poop3"]]
                        entity.PoopDamage = [30, 70, 100]

                    if settings["mode"].main != "MIXED":
                        for i in range(entity.PoopCount):      # 난이도 만큼 인스턴스 생성
                            entity.PoopList.append(Poop(entity.PoopImage, screen))
                    else:
                        for i in range(entity.PoopCount):
                            if i <= entity.PoopCount / 3:
                                entity.PoopList.append(Poop(entity.PoopImage[0], screen))
                            elif entity.PoopCount / 3 < i <= entity.PoopCount / 3 * 2:
                                entity.PoopList.append(Poop(entity.PoopImage[1], screen))
                            elif entity.PoopCount / 3 * 2 < i <= entity.PoopCount:
                                entity.PoopList.append(Poop(entity.PoopImage[2], screen))

                    for i in range(entity.ItemCount):      # 난이도 만큼 인스턴스 생성
                        entity.ItemList.append(AidKit(asset.item["aidkit"], screen))

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
                    settings_exit()
                    pygame.display.update()

                elif event.key == pygame.K_TAB:
                    settings_next()

                    # 선택 커서 구현 필요
                elif event.key == pygame.K_LALT:
                    settings[list(settings.keys())[SETTINGS.settings_index]].next()
                    break

                elif event.key == pygame.K_LSHIFT:
                    settings_reset()
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
                        if (playerKeyInit != "A"):
                            playerKeyInit = "A"
                            player.to_x = 0
                        player.to_x -= player.speed
                    if event.key == pygame.K_d:
                        if (playerKeyInit != "D"):
                            playerKeyInit = "D"
                            player.to_x = 0
                        player.to_x += player.speed
                if not player2.isDie():
                    if event.key == pygame.K_LEFT:            # <-는 왼쪽, ->는 오른쪽으로 이동
                        if (player2KeyInit != "LEFT"):
                            player2KeyInit = "LEFT"
                            player.to_x = 0
                        player2.to_x -= player.speed
                    if event.key == pygame.K_RIGHT:
                        if (player2KeyInit != "RIGHT"):
                            player2KeyInit = "RIGHT"
                            player.to_x = 0
                        player2.to_x += player.speed

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    playerKeyInit = None
                    player.to_x = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player2KeyInit = None
                    player2.to_x = 0
                
            if event.type == pygame.K_ESCAPE:
                pass
            
        # 만약 구역이 end 이라면
        elif area == areaList[4]:
            if event.type == pygame.KEYDOWN:    # 키가 눌렸을 때
                if event.key == pygame.K_SPACE:        # 스페이스 바를 눌렀을 때, 초기화 및 초기 화면
                    area = areaList[0]
                    isGameOver = False
                    player.reset()
                    player2.reset()
                    entity.PoopCount = 0
                    entity.PoopList = []
                    entity.ItemCount = 0
                    entity.ItemList = []
                    pygame.display.update()

    # title 구역
    if area == areaList[0]:
        sound.setMusicTheme()
        background, background_filter = loadBackground(asset.background["darken"], asset.background["filter"]["on_title"])  # 블러된 배경화면 로딩

        screen.blit(background, (0, 0))
        screen.blit(background_filter, (0, 0))
        screen.blit(fpscounter, (screen_width - 65, 5))

    # setting 구역
    elif area == areaList[1]:
        for i in settings.keys():
            settings[i].isSelect()

        background, background_filter = loadBackground(asset.background["darken"], asset.background["filter"]["on_setting"])
        game_font = pygame.font.Font(asset.font["NeoDunggeunmo"], 17)

        lang_config = settings["language"].main
        screen.blit(background, (0, 0))
        screen.blit(background_filter, (0, 0))
        screen.blit(fpscounter, (screen_width - 65, 5))
        screen.blit(settings["mode"].render_update(lang_config), (screen_width / 4 + 45, screen_height / 2 + -15)) # 20 간격
        screen.blit(settings["difficulty"].render_update(lang_config), (screen_width / 4 + 45, screen_height / 2 + 10))
        screen.blit(settings["player_type"].render_update(lang_config), (screen_width / 4 + 45, screen_height / 2 + 30))
        screen.blit(settings["score_type"].render_update(lang_config), (screen_width / 4 + 45, screen_height / 2 + 50))
        screen.blit(settings["background_theme"].render_update(lang_config), (screen_width / 4 + 5, screen_height / 2 + 100))
        screen.blit(settings["background_solid"].render_update(lang_config), (screen_width / 4 + 5, screen_height / 2 + 120))
        screen.blit(settings["use_sound"].render_update(lang_config), (screen_width / 2 + 150, screen_height / 2 + -15))
        screen.blit(settings["volume"].render_update(lang_config), (screen_width / 2 + 150, screen_height / 2 + 5))
        screen.blit(settings["fps_show"].render_update(lang_config), (screen_width / 2 + 150, screen_height / 2 + 25))
        screen.blit(settings["fps_set"].render_update(lang_config), (screen_width / 2 + 150, screen_height / 2 + 45))
        screen.blit(settings["language"].render_update(lang_config), (screen_width / 2 + 150, screen_height / 2 + 65))

    # info 구역
    elif area == areaList[2]:
        background, background_filter = loadBackground(asset.background["darken"], asset.background["filter"]["on_info"])
        screen.blit(background, (0, 0))
        screen.blit(background_filter, (0, 0))
        screen.blit(fpscounter, (screen_width - 65, 5))
        
    # start 구역
    elif area == areaList[3]:
        if not sound.isStart:
            sound.play()
        
        background = loadBackground(asset.background["default"])[0]       # 배경화면 로딩
        screen.blit(background, (0, 0))

        if settings["player_type"].main == "Single":
            if player.checkLevel() < 3 and sound.isToned:
                sound.stop()
                sound.reset()
                sound.play()

            if player.checkLevel() == 3 and not sound.isToned:
                sound.stop()
                sound.toneUp()
                sound.play()

        elif settings["player_type"].main == "Multi":
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
        for index, ItemInst in enumerate(entity.ItemList):
            ItemInst.move(dt)
            ItemInst.setRect()
            if player.rect.colliderect(ItemInst.rect) and not player.isDie():
                player.giveHeal(ItemInst.heal)
                del entity.ItemList[index]
                isDeleted = True
            if settings["player_type"].main == "Multi":
                if player2.rect.colliderect(ItemInst.rect) and not player2.isDie():
                    player2.giveHeal(ItemInst.heal)
                    if not isDeleted:
                        del entity.ItemList[index]
                        isDeleted = True

            if isDeleted:
                continue

            if not ItemInst.isOnLand(dt):
                del entity.ItemList[index]
            ItemInst.draw()
            isDeleted = False

        isDeleted = False
        delObj = []
        for index, PoopInst in enumerate(entity.PoopList):
            PoopInst.move(dt)
            PoopInst.setRect()
            if player.rect.colliderect(PoopInst.rect) and not player.isDie():  # 충돌 감지
                player.giveDamage(PoopInst.damage)
                delObj.append(entity.PoopList[index])
                del entity.PoopList[index]
                isDeleted = True
            if settings["player_type"].main == "Multi" and not player2.isDie():
                if player2.rect.colliderect(PoopInst.rect):
                    player2.giveDamage(PoopInst.damage)
                    if not isDeleted:
                        delObj.append(entity.PoopList[index])
                        del entity.PoopList[index]
                        isDeleted = True
            if PoopInst.isDestroy():    # 소멸 감지
                delObj.append(entity.PoopList[index])
                del entity.PoopList[index]
                if settings["score_type"].main == "Difficulty":
                    if not player.isDie():
                        player.score += 1 / settings["difficulty"].main
                    if settings["player_type"].main == "Multi" and not player2.isDie():
                        player2.score += 1 / settings["difficulty"].main
                else:
                    player.score += 1
                    if settings["player_type"].main == "Multi" and not player2.isDie():
                        player2.score += 1

            isDeleted = False
        
        if player.isDie():
            player.hideEntity()
        else:
            player.showEntity()
        
        if settings["player_type"].main == "Multi":
            if player2.isDie():
                player2.hideEntity()
            else:
                player2.showEntity()

        isGameOver = player.isDie()
        if settings["player_type"].main == "Multi":
            isGameOver = player.isDie() and player2.isDie()

        for PoopInst in entity.PoopList:
            if isGameOver:
                PoopInst.reset()
            PoopInst.draw() # 출력
        
        for ItemInst in entity.ItemList:
            if isGameOver:
                ItemInst.reset()
            ItemInst.draw() # 출력

        if isGameOver:      # 게임 오버시
            area = areaList[4]  # 게임 오버 화면으로 이동
            pygame.display.update()

        if len(entity.ItemList) != entity.ItemCount: 
            for i in range(entity.ItemCount - len(entity.ItemList)):
                entity.ItemList.append(AidKit(asset.item["aidkit"], screen))

        if len(entity.PoopList) != entity.PoopCount:
            for i in range(entity.PoopCount - len(entity.PoopList)):  
                if settings["mode"].main != "MIXED":
                    entity.PoopList.append(Poop(entity.PoopImage, screen))
                else:
                    if delObj[i].image_str == entity.PoopImage[0]:
                        entity.PoopList.append(Poop(entity.PoopImage[0], screen))
                    elif delObj[i].image_str == entity.PoopImage[1]:
                        entity.PoopList.append(Poop(entity.PoopImage[1], screen))
                    elif delObj[i].image_str == entity.PoopImage[2]:
                        entity.PoopList.append(Poop(entity.PoopImage[2], screen))
        
        game_font = pygame.font.Font(asset.font["NeoDunggeunmo"], 30)
        scoreboard = game_font.render("P1: Score: " + str(round(player.score, 2)), True, (255, 255, 255))   # 점수를 화면에 렌더링
        screen.blit(scoreboard, (10, 10))
        healthboard = game_font.render("P1: HP: " + str(player.health), True, (255, 255, 255))   # 점수를 화면에 렌더링
        screen.blit(healthboard, (10, 35))
        if settings["player_type"].main == "Multi":
            scoreboard2 = game_font.render("P2: Score: " + str(round(player2.score, 2)), True, (255, 255, 255))   # 점수를 화면에 렌더링
            screen.blit(scoreboard2, (screen_width / 2 + 35, 10))
            healthboard2 = game_font.render("P2: HP: " + str(player2.health), True, (255, 255, 255))   # 점수를 화면에 렌더링
            screen.blit(healthboard2, (screen_width / 2 + 35, 35))
        screen.blit(fpscounter, (screen_width - 65, 5))

    # end 구역
    elif area == areaList[4]:
        sound.stop()
        sound.reset()
        background, background_filter = loadBackground(asset.background["darken"], asset.background["filter"]["on_end"])       # 블러 배경화면 로딩
        screen.blit(background, (0, 0))
        screen.blit(background_filter, (0, 0))
        screen.blit(fpscounter, (screen_width - 65, 5))

        player.score = round(player.score, 2)
        player2.score = round(player2.score, 2)
        game_font = pygame.font.Font(asset.font["NeoDunggeunmo"], 30)
        finalScore = game_font.render("P1: Score: " + str(player.score), True, (255, 255, 255))   # 최종 점수 렌더링
        screen.blit(finalScore, (screen_width / 3, screen_height / 2 + 45))
        if settings["player_type"].main == "Multi":
            finalScore2 = game_font.render("P2: Score: " + str(player2.score), True, (255, 255, 255))   # 최종 점수 렌더링
            screen.blit(finalScore2, (screen_width / 3, screen_height / 2 + 80))
    
    # while문을 돌때 마다 각 함수와 변수를 업데이트 (pygame 시스템)
    pygame.display.update()

# while문에서 나왔을 때 바로 종료
pygame.quit()