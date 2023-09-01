import asset
import pygame
setting_font = pygame.font.Font(asset.font["NeoDunggeunmo"], 22)

class root():
    def __init__(self):
        self.main = None
        self.selection:list = None
        self.localization:dict = None
        self.color = (255, 255, 255)
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

    def next(self):
        if len(self.selection) - 1 == self.selection_index:
            self.selection_index = 0
        else:
            self.selection_index += 1
        self.main = self.selection[self.selection_index]
    
    def render_update(self, lang):
        self.text_render = setting_font.render(str(self.localization[lang][self.selection_index]), True, self.color)
        return self.text_render

# 기본 설정
class Mode(root):
    def __init__(self):
        super().__init__()
        self.selection = ["Normal", "Poison", "Radiation", "MIXED"]
        self.localization = {
            "En-US": ["Normal", "Poison", "Radiation", "MIXED"], 
            "Ko-KR": ["일반", "독성", "방사성", "믹스"]
        }
        self.main = self.selection[self.selection_index]

class Difficulty(root):
    def __init__(self):
        super().__init__()
        self.selection = [2, 3, 4, 1]
        self.localization = {
            "En-US": [2, 3, 4, 1],
            "Ko-KR": [2, 3, 4, 1]
        }
        self.main = self.selection[self.selection_index]

class PlayerType(root):
    def __init__(self):
        super().__init__()
        self.selection = ["Single", "Multi"]
        self.localization = {
            "En-US": ["Solo", "Duo"],
            "Ko-KR": ["솔로", "듀오"]
        }
        self.main = self.selection[self.selection_index]

class ScoreType(root):
    def __init__(self):
        super().__init__()
        self.selection = ["Count", "Difficulty"]
        self.localization = {
            "En-US": ["Count", "Difficulty"],
            "Ko-KR": ["일반","난이도순"]
        }
        self.selection_index = 0;
        self.main = self.selection[self.selection_index]

class UseSound(root):
    def __init__(self):
        super().__init__()
        self.selection = [True, False]
        self.localization = {
            "En-US": ["On", "Off"],
            "Ko-KR": ["켜기", "끄기"]
        }
        self.main = self.selection[self.selection_index]

class Volume(root):
    def __init__(self):
        super().__init__()
        self.selection = [60, 80, 100, 0, 20, 40]
        self.localization = {
            "En-US": [60, 80, 100, 0, 20, 40],
            "Ko-KR": [60, 80, 100, 0, 20, 40]
        }
        self.main = self.selection[self.selection_index]

class BackgroundTheme(root):
    def __init__(self):
        super().__init__()
        self.selection = ["LIGHT", "DARK"]
        self.localization = {
            "En-US": ["Light", "Dark"],
            "Ko-KR": ["라이트", "다크"]
        }
        self.main = self.selection[self.selection_index]

class BackgroundSolid(root):
    def __init__(self):
        super().__init__()
        self.selection = [False, True]
        self.localization = {
            "En-US": ["Off", "On"],
            "Ko-KR": ["끄기", "켜기"]
        }
        self.main = self.selection[self.selection_index]

class FpsShow(root):
    def __init__(self):
        super().__init__()
        self.selection = [False, True]
        self.localization = {
            "En-US": ["Off", "On"],
            "Ko-KR": ["끄기", "켜기"]
        }
        self.main = self.selection[self.selection_index]

class FpsSet(root):
    def __init__(self):
        super().__init__()
        self.selection = [144, 10, 20, 30, 60]
        self.localization = {
            "En-US": [144, 10, 20, 30, 60],
            "Ko-KR": [144, 10, 20, 30, 60]
        }
        self.main = self.selection[self.selection_index]

class Language(root):
    def __init__(self):
        super().__init__()
        self.selection = ["Ko-KR", "En-US"]
        self.localization = {
            "En-US": ["Korean", "English"],
            "Ko-KR": ["한국어", "영어"]
        }
        self.main = self.selection[self.selection_index]

def settings_next():
    global settings_index
    if len(list(settings.keys())) - 1 == settings_index:
        settings_index = 0
        settings[list(settings.keys())[settings_index]].isSelect(True)
        settings[list(settings.keys())[len(settings.keys()) - 1]].isSelect(False)
    else:
        settings_index += 1
        settings[list(settings.keys())[settings_index]].isSelect(True)
        settings[list(settings.keys())[settings_index - 1]].isSelect(False)

def settings_exit():
    global settings_index
    settings_index = 0
    for i in settings.keys():
        settings[i].isSelect(False)
    settings["mode"].isSelect(True)

def settings_reset():
    for i in settings.keys():
        settings[i].selection_index = 0
        settings[i].main = settings[i].selection[settings[i].selection_index]

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
    "volume": Volume(),
    "fps_show": FpsShow(),
    "fps_set": FpsSet(),
    "language": Language(),
}