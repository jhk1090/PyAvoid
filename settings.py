import asset
import pygame
setting_font = pygame.font.Font(asset.font["NeoDunggeunmo"], 22)

class root():
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

    def isSelect(self, select=None):
        if select != None:
            self.selected = select
        if self.selected:
            self.color = (86, 255, 86)
        else:
            self.color = (255, 255, 255)
        self.text_render = setting_font.render(str(self.main), True, self.color)

# 기본 설정
class Mode(root):
    def __init__(self):
        super().__init__()
        self.main = "Normal"                 # 모드(추가 예정)
        self.selection = ["Normal", "Poison", "Radiation", "MIXED"]
        self.text_render = setting_font.render(str(self.main), True, self.color)

class Difficulty(root):
    def __init__(self):
        super().__init__()
        self.main = 2              # 난이도 
        self.selection = [2, 3, 4, 1]
        self.text_render = setting_font.render(str(self.main), True, self.color)

class PlayerType(root):
    def __init__(self):
        super().__init__()
        self.main = "Single"      # 플레이어 모드
        self.selection = ["Single", "Multi"]
        self.text_render = setting_font.render(str(self.main), True, self.color)

class ScoreType(root):
    def __init__(self):
        super().__init__()
        self.main = "Difficulty"   # 점수 환산 방식
        self.selection = ["Difficulty", "Count"]
        self.text_render = setting_font.render(str(self.main), True, self.color)

class UseSound(root):
    def __init__(self):
        super().__init__()
        self.main = True            # 브금 여부
        self.selection = [True, False]
        self.text_render = setting_font.render(str(self.main), True, self.color)

class BackgroundTheme(root):
    def __init__(self):
        super().__init__()
        self.main = "LIGHT"              # 테마 
        self.selection = ["LIGHT", "DARK"]
        self.text_render = setting_font.render(str(self.main), True, self.color)

class BackgroundSolid(root):
    def __init__(self):
        super().__init__()
        self.main = False    # 단색 배경 사용
        self.selection = [False, True]
        self.text_render = setting_font.render(str(self.main), True, self.color)

class FpsShow(root):
    def __init__(self):
        super().__init__()
        self.main = True             # fps 표시 여부
        self.selection = [True, False]
        self.text_render = setting_font.render(str(self.main), True, self.color)

class FpsSet(root):
    def __init__(self):
        super().__init__()
        self.main = 144                # fps 설정
        self.selection = [144, 10, 20, 30, 60]
        self.text_render = setting_font.render(str(self.main), True, self.color)

class Language(root):
    def __init__(self):
        super().__init__()
        self.main = "En-US"
        self.selection = ["En-US", "Ko-KR"]
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