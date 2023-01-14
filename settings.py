import asset
import pygame
setting_font = pygame.font.Font(asset.font["NeoDunggeunmo"], 22)

class root():
    def __init__(self):
        self.main = None
        self.selection:list = None
        self.localization:dict = None
        self.color = (255, 255, 255)
        self.text_render = setting_font.render(str(self.main), True, self.color)
        self.selected = False
        self.selection_index:int = 0

    def reload(self, main=None, selection=None, text_render=None):
        self.main = main
        self.selection = selection
        self.text_render = text_render

    def isSelect(self, select=None):
        if select != None:
            self.selected = select
        if self.selected:
            self.color = (86, 255, 86)
        else:
            self.color = (255, 255, 255)
        self.text_render = setting_font.render(str(self.main), True, self.color)

    def nextOption(self):
        pass

# 기본 설정
class Mode(root):
    def __init__(self):
        super().__init__()
        self.main = "Normal"                 # 모드(추가 예정)
        self.selection = ["Normal", "Poison", "Radiation", "MIXED"]
        self.localization = {
            "En-US": ["Normal", "Poison", "Radiation", "MIXED"], 
            "Ko-KR": ["일반", "독성", "방사성", "믹스"]
        }
        self.text_render = setting_font.render(str(self.main), True, self.color)

class Difficulty(root):
    def __init__(self):
        super().__init__()
        self.main = 2              # 난이도 
        self.selection = [2, 3, 4, 1]
        self.localization = {
            "En-US": [1, 2, 3, 4],
            "Ko-KR": [1, 2, 3, 4]
        }
        self.text_render = setting_font.render(str(self.main), True, self.color)

class PlayerType(root):
    def __init__(self):
        super().__init__()
        self.main = "Single"      # 플레이어 모드
        self.selection = ["Single", "Multi"]
        self.localization = {
            "En-US": ["Solo", "Duo"],
            "Ko-KR": ["솔로", "듀오"]
        }
        self.text_render = setting_font.render(str(self.main), True, self.color)

class ScoreType(root):
    def __init__(self):
        super().__init__()
        self.main = "Difficulty"   # 점수 환산 방식
        self.selection = ["Difficulty", "Count"]
        self.localization = {
            "En-US": ["Difficulty", "Count"],
            "Ko-KR": ["난이도순", "일반"]
        }
        self.text_render = setting_font.render(str(self.main), True, self.color)

class UseSound(root):
    def __init__(self):
        super().__init__()
        self.main = True            # 브금 여부
        self.selection = [True, False]
        self.localization = {
            "En-US": ["On", "Off"],
            "Ko-KR": ["켜기", "끄기"]
        }
        self.text_render = setting_font.render(str(self.main), True, self.color)

class BackgroundTheme(root):
    def __init__(self):
        super().__init__()
        self.main = "LIGHT"              # 테마 
        self.selection = ["LIGHT", "DARK"]
        self.localization = {
            "En-US": ["Light", "Dark"],
            "Ko-KR": ["라이트", "다크"]
        }
        self.text_render = setting_font.render(str(self.main), True, self.color)

class BackgroundSolid(root):
    def __init__(self):
        super().__init__()
        self.main = False    # 단색 배경 사용
        self.selection = [False, True]
        self.localization = {
            "En-US": ["On", "Off"],
            "Ko-KR": ["켜기", "끄기"]
        }
        self.text_render = setting_font.render(str(self.main), True, self.color)

class FpsShow(root):
    def __init__(self):
        super().__init__()
        self.main = True             # fps 표시 여부
        self.selection = [True, False]
        self.localization = {
            "En-US": ["On", "Off"],
            "Ko-KR": ["켜기", "끄기"]
        }
        self.text_render = setting_font.render(str(self.main), True, self.color)

class FpsSet(root):
    def __init__(self):
        super().__init__()
        self.main = 144                # fps 설정
        self.selection = [144, 10, 20, 30, 60]
        self.localization = {
            "En-US": [10, 20, 30, 60, 144],
            "Ko-KR": [10, 20, 30, 60, 144]
        }
        self.text_render = setting_font.render(str(self.main), True, self.color)

class Language(root):
    def __init__(self):
        super().__init__()
        self.main = "En-US"
        self.selection = ["En-US", "Ko-KR"]
        self.localization = {
            "En-US": ["English", "Korean"],
            "Ko-KR": ["영어", "한국어"]
        }
        self.text_render = setting_font.render(str(self.main), True, self.color)

settings_index: int  = 0
settings: dict = {
    # in-game
    "mode": Mode(),
    "difficulty": Difficulty(),
    "player_type": PlayerType(),
    "score_type": ScoreType(),
    "background_theme": BackgroundTheme(),
    "background_solid": BackgroundSolid(),
    # preference
    "use_sound": UseSound(),
    "fps_show": FpsShow(),
    "fps_set": FpsSet(),
    "language": Language()
}