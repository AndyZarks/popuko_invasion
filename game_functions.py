import sys
import pygame
from time import sleep
from bullet import Bullet
from alien import Alien


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """处理按键按下事件"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    """处理按键松开事件"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """监测事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # 点击关闭窗口键将结束游戏
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            # 检测按键按下
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            # 检测按键抬起
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 检测鼠标按键按下
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """当玩家单击play按钮时开始游戏"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()

        # 隐藏光标
        pygame.mouse.set_visible(False)

        # 重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        # 重置计分板图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    """屏幕绘制"""
    # 绘制背景
    screen.fill(ai_settings.bg_color)

    # 绘制所有的子弹
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    # 绘制飞船和外星人
    ship.blitme()
    aliens.draw(screen)

    # 显示得分
    sb.show_score()

    # 如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()

    # 使最近绘制的屏幕可见
    pygame.display.flip()


def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """更新外星人群中所有外星人的位置"""
    # 检查是否有外星人处于屏幕边缘，并更新全体外星人的位置
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)

    # 检测外星人是否碰到屏幕底部
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)


def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 同飞船被撞到一样处理
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
            break


def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        # 将ship_left减1
        stats.ships_left -= 1

        # 更新飞船数量
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # 暂停
        sleep(0.3)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """更新子弹位置，并删除已经消失的子弹"""
    bullets.update()
    # 检查是否有子弹超出窗口范围，如果有，删除该子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """相应子弹和外星人的碰撞"""
    # 当子弹击中了敌人，删除相应的子弹和外星人，并记录到字典里
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)  # 两个实参True分别告诉Pygame删除子弹和外星人
    # 将每一个被消灭的外星人都纳入记分
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        # 检查是否产生了新的最高分
        check_high_score(stats, sb)
    # 检测是否所有外星人都被消灭了
    # 如果是，开始新的关卡
    if len(aliens) == 0:
        start_new_level(ai_settings, screen, stats, sb, ship, aliens, bullets)


def start_new_level(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """开始新的关卡"""
    bullets.empty()
    ai_settings.increase_speed()
    stats.level += 1
    sb.prep_level()
    create_fleet(ai_settings, screen, ship, aliens)


def fire_bullet(ai_settings, screen, ship, bullets):
    """创建一颗子弹并加入编组bullets"""
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
    """计算一行可以容纳多少个外星人"""
    # 屏幕两边各空出一个外星人宽度的距离，外星人之间的间距为外星人宽度
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可以容纳多少行外星人"""
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows - 1


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """创建一个外星人并将其加入当前行"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = 2 * alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人舰队群"""
    # 创建一个外星人对象
    alien = Alien(ai_settings, screen)
    # 计算一行可以容纳多少个外星人
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    # 计算屏幕可以容纳多少行外星人
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # 创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时应采取的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    """将整体外星人下移并改变它们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_high_score(stats, sb):
    """检查是否诞生了新的最高分"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
