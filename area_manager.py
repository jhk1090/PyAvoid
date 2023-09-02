from settings import settings
from entity import Poop, AidKit
import entity
import pygame
import asset
import init
from pygame.locals import *


def call():
    # fps 설정
    dt = init.clock.tick(settings["fps_set"].main)
    # fps 구하기
    fps = init.clock.get_fps()
    fontfps = pygame.font.Font(asset.font["NeoDunggeunmo"], 20)
    if (settings["fps_show"]).main:
        fpscounter = fontfps.render(
            f"{int(fps)}fps", True, (255, 255, 255))        # fps 화면에 렌더링
    else:
        fpscounter = fontfps.render("", True, (255, 255, 255))

    # title 구역
    if init.area == init.areaList[0]:
        areaTitle(fpscounter)

    # setting 구역
    elif init.area == init.areaList[1]:
        areaSetting(fpscounter)

    # info 구역
    elif init.area == init.areaList[2]:
        areaInfo(fpscounter)

    # start 구역
    elif init.area == init.areaList[3]:
        areaStart(fpscounter, dt)

    # end 구역
    elif init.area == init.areaList[4]:
        areaEnd(fpscounter)


def areaTitle(fpscounter):
    init.sound.setMusicTheme()
    background, background_filter = init.loadBackground(
        asset.background["darken"], asset.background["filter"]["on_title"])  # 블러된 배경화면 로딩

    init.screen.blit(background, (0, 0))
    init.screen.blit(background_filter, (0, 0))
    init.screen.blit(fpscounter, (init.screen_width - 65, 5))


def areaSetting(fpscounter):
    for i in settings.keys():
        settings[i].isSelect()

    background, background_filter = init.loadBackground(
        asset.background["darken"], asset.background["filter"]["on_setting"])
    game_font = pygame.font.Font(asset.font["NeoDunggeunmo"], 17)

    lang_config = settings["language"].main
    init.screen.blit(background, (0, 0))
    init.screen.blit(background_filter, (0, 0))
    init.screen.blit(fpscounter, (init.screen_width - 65, 5))
    init.screen.blit(settings["mode"].render_update(
        lang_config), (init.screen_width / 4 + 45, init.screen_height / 2 + -15))  # 20 간격
    init.screen.blit(settings["difficulty"].render_update(
        lang_config), (init.screen_width / 4 + 45, init.screen_height / 2 + 10))
    init.screen.blit(settings["player_type"].render_update(
        lang_config), (init.screen_width / 4 + 45, init.screen_height / 2 + 30))
    init.screen.blit(settings["score_type"].render_update(
        lang_config), (init.screen_width / 4 + 45, init.screen_height / 2 + 50))
    init.screen.blit(settings["background_theme"].render_update(
        lang_config), (init.screen_width / 4 + 5, init.screen_height / 2 + 100))
    init.screen.blit(settings["background_solid"].render_update(
        lang_config), (init.screen_width / 4 + 5, init.screen_height / 2 + 120))
    init.screen.blit(settings["use_sound"].render_update(
        lang_config), (init.screen_width / 2 + 150, init.screen_height / 2 + -15))
    init.screen.blit(settings["volume"].render_update(
        lang_config), (init.screen_width / 2 + 150, init.screen_height / 2 + 5))
    init.screen.blit(settings["fps_show"].render_update(
        lang_config), (init.screen_width / 2 + 150, init.screen_height / 2 + 25))
    init.screen.blit(settings["fps_set"].render_update(
        lang_config), (init.screen_width / 2 + 150, init.screen_height / 2 + 45))
    init.screen.blit(settings["language"].render_update(
        lang_config), (init.screen_width / 2 + 150, init.screen_height / 2 + 65))


def areaInfo(fpscounter):
    background, background_filter = init.loadBackground(
        asset.background["darken"], asset.background["filter"]["on_info"])
    init.screen.blit(background, (0, 0))
    init.screen.blit(background_filter, (0, 0))
    init.screen.blit(fpscounter, (init.screen_width - 65, 5))


def areaStart(fpscounter, dt):
    if not init.sound.isStart:
        init.sound.play()

    init.sound.stop() if init.isPause else ""

    background, background_filter = init.loadBackground(
        asset.background["default"], asset.background["filter"]["on_pause"])       # 배경화면 로딩
    background_darken = init.loadBackground(asset.background["darken"])[0]
    init.screen.blit(background_darken, (0, 0)
                     ) if init.isPause else init.screen.blit(background, (0, 0))

    if settings["player_type"].main == "Single":
        if init.player.checkLevel() < 3 and init.sound.isToned:
            init.sound.stop()
            init.sound.reset()
            init.sound.play()

        if init.player.checkLevel() == 3 and not init.sound.isToned:
            init.sound.stop()
            init.sound.toneUp()
            init.sound.play()

    elif settings["player_type"].main == "Multi":
        if (init.player.checkLevel() < 3 or init.player.isDie()) and (init.player2.checkLevel() < 3 or init.player2.isDie()) and init.sound.isToned:
            init.sound.stop()
            init.sound.reset()
            init.sound.play()

        if (init.player.checkLevel() == 3 or init.player2.checkLevel() == 3) and not init.sound.isToned:
            init.sound.stop()
            init.sound.toneUp()
            init.sound.play()

        init.player2.move(dt) if not init.isPause else ""
        init.player2.limitPos()
        init.player2.setRect()
        init.player2.draw()

    init.player.move(dt) if not init.isPause else ""     # 프레임을 인자로 해서 이동
    init.player.limitPos()   # 제한되는 지 확인
    init.player.setRect()    # rect 설정하기
    init.player.draw()       # 출력

    isDeleted = False
    for index, ItemInst in enumerate(entity.ItemList):
        ItemInst.move(dt) if not init.isPause else ""
        ItemInst.setRect()
        if init.player.rect.colliderect(ItemInst.rect) and not init.player.isDie():
            init.player.giveHeal(ItemInst.heal)
            del entity.ItemList[index]
            isDeleted = True
        if settings["player_type"].main == "Multi":
            if init.player2.rect.colliderect(ItemInst.rect) and not init.player2.isDie():
                init.player2.giveHeal(ItemInst.heal)
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
        PoopInst.move(dt) if not init.isPause else ""
        PoopInst.setRect()
        # 충돌 감지
        if init.player.rect.colliderect(PoopInst.rect) and not init.player.isDie():
            init.player.giveDamage(PoopInst.damage)
            delObj.append(entity.PoopList[index])
            del entity.PoopList[index]
            isDeleted = True
        if settings["player_type"].main == "Multi" and not init.player2.isDie():
            if init.player2.rect.colliderect(PoopInst.rect):
                init.player2.giveDamage(PoopInst.damage)
                if not isDeleted:
                    delObj.append(entity.PoopList[index])
                    del entity.PoopList[index]
                    isDeleted = True
        if PoopInst.isDestroy():    # 소멸 감지
            delObj.append(entity.PoopList[index])
            del entity.PoopList[index]
            if settings["score_type"].main == "Difficulty":
                if not init.player.isDie():
                    init.player.score += 1 / settings["difficulty"].main
                if settings["player_type"].main == "Multi" and not init.player2.isDie():
                    init.player2.score += 1 / settings["difficulty"].main
            else:
                init.player.score += 1
                if settings["player_type"].main == "Multi" and not init.player2.isDie():
                    init.player2.score += 1

        isDeleted = False

    if init.player.isDie():
        init.player.hideEntity()
    else:
        init.player.showEntity()

    if settings["player_type"].main == "Multi":
        if init.player2.isDie():
            init.player2.hideEntity()
        else:
            init.player2.showEntity()

    isGameOver = init.player.isDie()
    if settings["player_type"].main == "Multi":
        isGameOver = init.player.isDie() and init.player2.isDie()

    for PoopInst in entity.PoopList:
        if isGameOver:
            PoopInst.reset()
        PoopInst.draw()  # 출력

    for ItemInst in entity.ItemList:
        if isGameOver:
            ItemInst.reset()
        ItemInst.draw()  # 출력

    if isGameOver:      # 게임 오버시
        init.area = init.areaList[4]  # 게임 오버 화면으로 이동
        pygame.display.update()

    if len(entity.ItemList) != entity.ItemCount:
        for i in range(entity.ItemCount - len(entity.ItemList)):
            entity.ItemList.append(AidKit(asset.item["aidkit"], init.screen))

    if len(entity.PoopList) != entity.PoopCount:
        for i in range(entity.PoopCount - len(entity.PoopList)):
            if settings["mode"].main != "MIXED":
                entity.PoopList.append(Poop(entity.PoopImage, init.screen))
            else:
                if delObj[i].image_str == entity.PoopImage[0]:
                    entity.PoopList.append(
                        Poop(entity.PoopImage[0], init.screen))
                elif delObj[i].image_str == entity.PoopImage[1]:
                    entity.PoopList.append(
                        Poop(entity.PoopImage[1], init.screen))
                elif delObj[i].image_str == entity.PoopImage[2]:
                    entity.PoopList.append(
                        Poop(entity.PoopImage[2], init.screen))

    game_font = pygame.font.Font(asset.font["NeoDunggeunmo"], 30)
    scoreboard = game_font.render(
        "P1: Score: " + str(round(init.player.score, 2)), True, (255, 255, 255))   # 점수를 화면에 렌더링
    init.screen.blit(scoreboard, (10, 10))
    healthboard = game_font.render(
        "P1: HP: " + str(init.player.health), True, (255, 255, 255))   # 점수를 화면에 렌더링
    init.screen.blit(healthboard, (10, 35))
    if settings["player_type"].main == "Multi":
        scoreboard2 = game_font.render(
            "P2: Score: " + str(round(init.player2.score, 2)), True, (255, 255, 255))   # 점수를 화면에 렌더링
        init.screen.blit(scoreboard2, (init.screen_width / 2 + 35, 10))
        healthboard2 = game_font.render(
            "P2: HP: " + str(init.player2.health), True, (255, 255, 255))   # 점수를 화면에 렌더링
        init.screen.blit(healthboard2, (init.screen_width / 2 + 35, 35))
    init.screen.blit(fpscounter, (init.screen_width - 65, 5))
    init.screen.blit(background_filter, (0, 0)) if init.isPause else ""


def areaEnd(fpscounter):
    init.sound.stop()
    init.sound.reset()
    background, background_filter = init.loadBackground(
        asset.background["darken"], asset.background["filter"]["on_end"])       # 블러 배경화면 로딩
    background, background_record_filter = init.loadBackground(
        asset.background["darken"], asset.background["filter"]["on_end_record"])
    init.screen.blit(background, (0, 0))

    init.player.score = round(init.player.score, 2)
    init.player2.score = round(init.player2.score, 2)
    game_font = pygame.font.Font(asset.font["NeoDunggeunmo"], 30)
    game_font_emphasize = pygame.font.Font(asset.font["NeoDunggeunmo"], 45)
    WHITE = (255, 255, 255)
    GRAY = (170, 170, 170)
    GOLD = (249, 232, 104)
    SUBCOLOR = (0, 0, 0)
    scoreDiff = init.player.score - init.HIGHSCORE
    renderedSubString = ""
    renderedFilter = background_filter
    if scoreDiff > 0:
        SUBCOLOR = GOLD
        renderedSubString = f"{str(init.HIGHSCORE)} (+{str(scoreDiff)})"
        renderedFilter = background_record_filter
    else:
        SUBCOLOR = GRAY
        renderedSubString = f"{str(init.HIGHSCORE)} ({str(scoreDiff)})"

    init.screen.blit(renderedFilter, (0, 0))
    init.screen.blit(fpscounter, (init.screen_width - 65, 5))

    if settings["player_type"].main == "Single":
        if settings["language"].main == "Ko-KR":
            score_label = game_font.render("점수: ", True, WHITE)
            score = game_font_emphasize.render(
                str(init.player.score), True, WHITE)
            score_label_high = game_font.render("개인 최고 기록: ", True, SUBCOLOR)
            score_high = game_font.render(renderedSubString, True, SUBCOLOR)

            init.screen.blit(score_label, (init.screen_width /
                             3 + 5, init.screen_height / 2 + 55))
            init.screen.blit(score, (init.screen_width / 2 +
                             20, init.screen_height / 2 + 45))
            init.screen.blit(
                score_label_high, (init.screen_width / 4 - 90, init.screen_height / 2 + 90))
            init.screen.blit(score_high, (init.screen_width /
                             2 + 20, init.screen_height / 2 + 90))
        elif settings["language"].main == "En-US":
            score_label = game_font.render("Score: ", True, WHITE)
            score = game_font_emphasize.render(
                str(init.player.score), True, WHITE)
            score_label_high = game_font.render(
                "Highest Score: ", True, SUBCOLOR)
            score_high = game_font.render(renderedSubString, True, SUBCOLOR)

            init.screen.blit(score_label, (init.screen_width /
                             3 - 20, init.screen_height / 2 + 55))
            init.screen.blit(score, (init.screen_width / 2 +
                             20, init.screen_height / 2 + 45))
            init.screen.blit(
                score_label_high, (init.screen_width / 4 - 80, init.screen_height / 2 + 90))
            init.screen.blit(score_high, (init.screen_width /
                             2 + 20, init.screen_height / 2 + 90))
    elif settings["player_type"].main == "Multi":
        finalScore = game_font.render(
            "P1: Score: " + str(init.player.score), True, WHITE)   # 최종 점수 렌더링
        init.screen.blit(finalScore, (init.screen_width /
                         3, init.screen_height / 2 + 45))
        finalScore2 = game_font.render(
            "P2: Score: " + str(init.player2.score), True, WHITE)   # 최종 점수 렌더링
        init.screen.blit(finalScore2, (init.screen_width /
                         3, init.screen_height / 2 + 80))
