# 엔티티
from pygame.locals import *
import pygame
import random
import asset
from settings import settings

screen_width = 480
screen_height = 640

class Entity():
    def __init__(self, image: str, scale: float, screen: pygame.Surface):
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
        self.screen = screen

    # 충돌 감지 비교 요소
    def setRect(self):
        self.rect = self.image.get_rect()
        self.rect.left = self.x
        self.rect.top = self.y

    # 그리기
    def draw(self):
        self.screen.blit(self.image, (self.x, self.y))

    # 숨기기
    def hideEntity(self):
        self.image = pygame.image.load(asset.empty_image)

    # 보이기
    def showEntity(self):
        self.image = self.image_o

# 플레이어
class Player(Entity):
    def __init__(self, image, screen: pygame.Surface):
        super().__init__(image, 0.6, screen)
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
        game_font = pygame.font.Font(asset.font["NeoDunggeunmo"], 20)
        gotDamage = game_font.render("-" + str(damage), True, (255, 0, 0))
        self.screen.blit(gotDamage, (self.x + 15, self.y - 15))
        if self.health <= 0:
            self.health = 0
    
    # 체력 획득
    def giveHeal(self, health):
        self.health += health
        game_font = pygame.font.Font(asset.font["NeoDunggeunmo"], 20)
        gotHeal = game_font.render("+" + str(health), True, (0, 255, 0))
        self.screen.blit(gotHeal, (self.x + 15, self.y - 15))
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
    def __init__(self, image, screen: pygame.Surface):
        super().__init__(image, 0.8, screen)
        self.x = random.randint(0, screen_width - int(round(self.width)))
        self.y = 0 - self.height
        self.speed = (random.randint(1, 4)) / 10
        self.rect = None
        self.damage = 0;
        if settings["mode"].main == "MIXED":
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
        return self.y >= (screen_height - self.height)
        # return self.y > screen_height

    # 이동
    def move(self, frame):
        self.y += frame * self.speed

    # 초기화
    def reset(self):
        self.y = 0 - self.height

# 아이템
class Item(Entity):
    def __init__(self, image, screen: pygame.Surface):
        super().__init__(image, 0.8, screen)
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
    def __init__(self, image, screen: pygame.Surface):
        super().__init__(image, screen)
        self.x = random.randint(0, screen_width - int(round(self.width)))
        self.y = 0 - self.height
        self.speed = (random.randint(1, 4)) / 10
        self.heal = 5

PoopList = []   # 똥 인스턴스 생성 목록
PoopCount = 0   # 똥 갯수
PoopImage = asset.entity["poop"]
PoopDamage = 30
ItemList = []   # 아이템 인스턴스 생성 목록
ItemCount = 0   # 아이템 갯수