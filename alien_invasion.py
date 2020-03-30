import pygame
import game_functions as gf
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from game_status import GameStats
from scoreboard import Scoreboard
from button import Button


def run_game():
    """初始化pygame，设置和屏幕对象"""
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("POP子入侵 - A Game Developed by AndyZarks")

    # 创建Play按钮
    play_button = Button(ai_settings, screen, "Play")
    # 创建一艘飞船
    ship = Ship(ai_settings, screen)
    # 创建存储外星人的编组
    aliens = Group()
    # 创建外星人舰队
    gf.create_fleet(ai_settings, screen, ship, aliens)
    # 创建存储子弹的编组
    bullets = Group()
    # 创建存储游戏统计信息的实例，并创建记分牌
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    # 设置游戏的刷新率
    fps = pygame.time.Clock()

    '''游戏的主循环'''
    while True:
        # 监听键盘鼠标事件
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            # 更新游戏单位的位置信息
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets)
        # 绘制新的屏幕
        fps.tick(60)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)


run_game()
