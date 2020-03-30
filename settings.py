class Settings():
    """存储游戏设置的类"""

    def __init__(self):
        """初始化游戏设置"""

        # 屏幕设置
        self.screen_width = 1280
        self.screen_height = 720
        self.bg_color = (230, 230, 230)

        # 飞船设置
        self.ship_limit = 3

        # 外星人设置
        self.fleet_drop_speed = 10

        # 子弹设置
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 5

        # 以什么样的速率加快游戏节奏
        self.speedup_scale = 1.1
        # 得分的提高速度
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随着游戏进行发生改变的数值"""
        self.ship_speed_factor = 5.5
        self.bullet_speed_factor = 7
        self.alien_speed_factor = 3.5
        self.fleet_direction = 1  # 值1表示右移 -1表示左移
        self.alien_points = 100

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
