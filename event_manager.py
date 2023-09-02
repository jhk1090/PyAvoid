import pygame
import asset

from settings import settings, settings_next, settings_exit, settings_reset
import settings as SETTINGS
import entity
import init
from entity import Poop, AidKit

moveLeft = False
moveRight = False
move2Left = False
move2Right = False
isMoved = False
is2Moved = False

def reset():
    global moveLeft, moveRight, move2Left, move2Right, isMoved, is2Moved
    moveLeft = False
    moveRight = False
    move2Left = False
    move2Right = False
    isMoved = False
    is2Moved = False
    init.isGameOver = False
    init.player.reset()
    init.player2.reset()
    entity.PoopCount = 0
    entity.PoopList = []
    entity.ItemCount = 0
    entity.ItemList = []
    pygame.display.update()

def call():
    global moveLeft, moveRight, move2Left, move2Right, isMoved, is2Moved
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
                    if event.key == pygame.K_a and not moveLeft:            # a는 왼쪽, d는 오른쪽으로 이동
                        moveLeft = True
                        moveRight = False
                        isMoved = False
                    if event.key == pygame.K_d and not moveRight:
                        moveRight = True
                        moveLeft = False
                        isMoved = False
                if not init.player2.isDie():
                    if event.key == pygame.K_LEFT and not move2Left:            # <-는 왼쪽, ->는 오른쪽으로 이동
                        move2Left = True
                        move2Right = False
                        is2Moved = False
                    if event.key == pygame.K_RIGHT and not move2Right:
                        move2Right = True
                        move2Left = False
                        is2Moved = False
                if event.key == pygame.K_ESCAPE and not init.isPause:
                    init.isPause = True
                if event.key == pygame.K_SPACE and init.isPause:
                    init.isPause = False
                if event.key == pygame.K_LCTRL and init.isPause:
                    init.area = init.areaList[0]
                    reset()
                    pygame.display.update()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a and moveLeft:
                    init.player.to_x = 0
                    moveLeft = False
                elif event.key == pygame.K_d and moveRight:
                    init.player.to_x = 0
                    moveRight = False
                elif event.key == pygame.K_LEFT and move2Left:
                    init.player2.to_x = 0
                    move2Left = False
                elif event.key == pygame.K_RIGHT and move2Right:
                    init.player2.to_x = 0
                    move2Right = False
                print("==UP==\n", init.player.to_x, moveLeft, moveRight, move2Left, move2Right, "\n====")
        # 만약 구역이 end 이라면
        elif init.area == init.areaList[4]:
            if event.type == pygame.KEYDOWN:    # 키가 눌렸을 때
                if event.key == pygame.K_SPACE:        # 스페이스 바를 눌렀을 때, 초기화 및 초기 화면
                    init.area = init.areaList[0]
                    reset()
                    
    if not isMoved:
        if moveLeft: init.player.to_x = init.player.speed * -1
        if moveRight: init.player.to_x = init.player.speed
        isMoved = True
    
    if not is2Moved:
        if move2Left: init.player2.to_x = init.player2.speed * -1
        if move2Right: init.player2.to_x = init.player2.speed
        is2Moved = True

    # if moveLeft or moveRight or move2Left or move2Right:
    #     print(init.player.to_x, moveLeft, moveRight, move2Left, move2Right)