import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """管理外星人单位的类，继承精灵(Sprite)类"""

    def __init__(self, ai_settings, screen):
        """初始化敌人并设置起始位置"""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载外星人图像，并设置rect属性
        self.image = pygame.image.load('images/alien.png')
        self.rect = self.image.get_rect()

        # 每个外星人最初都在屏幕左上角附近
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的准确位置
        self.x = float(self.rect.x)

    def update(self):
        """更新外星人位置信息"""
        self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """如果外星人处于屏幕边缘，就返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def blitme(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image, self.rect)
