import pygame
# 초기화
pygame.init()
pygame.mixer.init()

import os
import sys
import init
import area_manager
import event_manager

from pygame.locals import *

# 라이브러리
this_path = os.path.dirname(sys.argv[0])

while init.running:
    event_manager.call()
    area_manager.call()
    # while문을 돌때 마다 각 함수와 변수를 업데이트 (pygame 시스템)
    pygame.display.update()

# while문에서 나왔을 때 바로 종료
pygame.quit()