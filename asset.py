import os
import sys

this_path = os.path.dirname(sys.argv[0])

background = {
    "darken": [f"{this_path}\\asset\\background\\light\\darken.png",
               f"{this_path}\\asset\\background\\dark\\darken.png"],
    "default": [f"{this_path}\\asset\\background\\light\\default.png",
                f"{this_path}\\asset\\background\\dark\\default.png"],
    "solid": [f"{this_path}\\asset\\background\\light\\solid.png",
              f"{this_path}\\asset\\background\\dark\\solid.png"],
    "filter": {
        "on_title": [f"{this_path}\\asset\\background\\filter\\en\\on_title.png",
                     f"{this_path}\\asset\\background\\filter\\ko\\on_title.png",],
        "on_end": [f"{this_path}\\asset\\background\\filter\\en\\on_end.png",
                   f"{this_path}\\asset\\background\\filter\\ko\\on_end.png",],
        "on_info": [f"{this_path}\\asset\\background\\filter\\en\\on_info.png",
                    f"{this_path}\\asset\\background\\filter\\ko\\on_info.png",],
        "on_setting": [f"{this_path}\\asset\\background\\filter\\en\\on_setting.png",
                       f"{this_path}\\asset\\background\\filter\\ko\\on_setting.png",]
    }
}

entity = {
    "poop": f"{this_path}\\asset\\entity\\poop.png",
    "poop2": f"{this_path}\\asset\\entity\\poop2.png",
    "poop3": f"{this_path}\\asset\\entity\\poop3.png",
    "sprite": f"{this_path}\\asset\\entity\\sprite.png",
    "sprite2": f"{this_path}\\asset\\entity\\sprite2.png"
}

item = {
    "aidkit": f"{this_path}\\asset\\item\\aidkit.png"
}

font = {
    "NeoDunggeunmo": f"{this_path}\\asset\\font\\NeoDunggeunmoPro-Regular.ttf"
}

sound = {
    "raving_energy": [f"{this_path}\\asset\\sound\\Raving_Energy.mp3",
                      f"{this_path}\\asset\\sound\\Raving_Energy_(faster).mp3",],
    "rollin_at_5": [f"{this_path}\\asset\\sound\\Rollin_at_5.mp3",
                    f"{this_path}\\asset\\sound\\Rollin_at_5_(electronic).mp3",]
}

empty_image = f"{this_path}\\asset\\empty.png"
