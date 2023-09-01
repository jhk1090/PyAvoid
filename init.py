import asset
from pygame.locals import *
import pygame

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

from settings import settings
from entity import Player

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

isPause = False