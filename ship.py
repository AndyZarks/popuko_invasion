import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """初始化飞船并设置起始位置"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 设置飞船的移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

        # 加载飞船图像并获取外接矩形
        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 将每艘新飞船放在屏幕底部中央位置
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # 在ship类的centerx和centery属性中存储浮点数值
        self.centerx = float(self.rect.centerx)
        self.centery = float(self.rect.centery)

    def blitme(self):
        """绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """根据移动标志调整飞船的位置"""

        # 更新ship类的centerx/y的值前加入判断条件，防止移动超出窗口范围
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.centerx -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.centery -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.ai_settings.ship_speed_factor

        # 根据centerx/y属性的值来更新rect对象，rect对象仅保留整数部分的值
        self.rect.centerx = self.centerx
        self.rect.centery = self.centery

    def center_ship(self):
        """让飞船在屏幕上居中"""
        self.centerx = self.screen_rect.centerx
        self.centery = self.screen_rect.bottom - self.rect.height
