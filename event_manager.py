import pygame
import asset

from settings import settings, settings_next, settings_exit, settings_reset
import settings as SETTINGS
import entity
import init
from entity import Poop, AidKit

def call():
    # 이벤트 관리
    for event in pygame.event.get():
        # 만약 X버튼을 눌렀을때
        if event.type == pygame.QUIT:
            init.running = False

        # 만약 구역이 title 이라면
        if init.area == init.areaList[0]:
            if event.type == pygame.KEYDOWN:    # 키를 눌렀을때
                if event.key == pygame.K_SPACE:
                    init.area = init.areaList[3]
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
                        entity.PoopImage = [
                            asset.entity["poop"], asset.entity["poop2"], asset.entity["poop3"]]
                        entity.PoopDamage = [30, 70, 100]

                    if settings["mode"].main != "MIXED":
                        for i in range(entity.PoopCount):      # 난이도 만큼 인스턴스 생성
                            entity.PoopList.append(
                                Poop(entity.PoopImage, init.screen))
                    else:
                        for i in range(entity.PoopCount):
                            if i <= entity.PoopCount / 3:
                                entity.PoopList.append(
                                    Poop(entity.PoopImage[0], init.screen))
                            elif entity.PoopCount / 3 < i <= entity.PoopCount / 3 * 2:
                                entity.PoopList.append(
                                    Poop(entity.PoopImage[1], init.screen))
                            elif entity.PoopCount / 3 * 2 < i <= entity.PoopCount:
                                entity.PoopList.append(
                                    Poop(entity.PoopImage[2], init.screen))

                    for i in range(entity.ItemCount):      # 난이도 만큼 인스턴스 생성
                        entity.ItemList.append(
                            AidKit(asset.item["aidkit"], init.screen))

                    pygame.display.update()
                elif event.key == pygame.K_LCTRL:
                    init.area = init.areaList[1]
                    pygame.display.update()
                elif event.key == pygame.K_LALT:
                    init.area = init.areaList[2]
                    pygame.display.update()

        # 만약 구역이 setting 이라면
        elif init.area == init.areaList[1]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    init.area = init.areaList[0]
                    settings_exit()
                    pygame.display.update()

                elif event.key == pygame.K_TAB:
                    settings_next()

                    # 선택 커서 구현 필요
                elif event.key == pygame.K_LALT:
                    settings[list(settings.keys())[
                        SETTINGS.settings_index]].next()
                    break

                elif event.key == pygame.K_LSHIFT:
                    settings_reset()
                    break

        # 만약 구역이 info 이라면
        elif init.area == init.areaList[2]:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    init.area = init.areaList[0]
                    pygame.display.update()

        # 만약 구역이 start 이라면
        elif init.area == init.areaList[3]:
            if event.type == pygame.KEYDOWN:    # 키가 눌렸을때
                if not init.player.isDie():
                    if event.key == pygame.K_a:            # a는 왼쪽, d는 오른쪽으로 이동
                        if (init.playerKeyInit != "A"):
                            init.playerKeyInit = "A"
                            init.player.to_x = 0
                        init.player.to_x -= init.player.speed
                    if event.key == pygame.K_d:
                        if (init.playerKeyInit != "D"):
                            init.playerKeyInit = "D"
                            init.player.to_x = 0
                        init.player.to_x += init.player.speed
                if not init.player2.isDie():
                    if event.key == pygame.K_LEFT:            # <-는 왼쪽, ->는 오른쪽으로 이동
                        if (init.player2KeyInit != "LEFT"):
                            init.player2KeyInit = "LEFT"
                            init.player2.to_x = 0
                        init.player2.to_x -= init.player.speed
                    if event.key == pygame.K_RIGHT:
                        if (init.player2KeyInit != "RIGHT"):
                            init.player2KeyInit = "RIGHT"
                            init.player2.to_x = 0
                        init.player2.to_x += init.player.speed
                if event.key == pygame.K_ESCAPE and not init.isPause:
                    init.isPause = True
                if event.key == pygame.K_SPACE and init.isPause:
                    init.isPause = False
                if event.key == pygame.K_LCTRL and init.isPause:
                    init.isPause = False
                    init.area = init.areaList[0]
                    init.player.reset()
                    init.player2.reset()
                    entity.PoopCount = 0
                    entity.PoopList = []
                    entity.ItemCount = 0
                    entity.ItemList = []
                    pygame.display.update()
                print(init.playerKeyInit, init.player.to_x)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    init.player.to_x = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    init.player2.to_x = 0

        # 만약 구역이 end 이라면
        elif init.area == init.areaList[4]:
            if event.type == pygame.KEYDOWN:    # 키가 눌렸을 때
                if event.key == pygame.K_SPACE:        # 스페이스 바를 눌렀을 때, 초기화 및 초기 화면
                    init.area = init.areaList[0]
                    init.isGameOver = False
                    init.player.reset()
                    init.player2.reset()
                    entity.PoopCount = 0
                    entity.PoopList = []
                    entity.ItemCount = 0
                    entity.ItemList = []
                    pygame.display.update()
