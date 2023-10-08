class Settings():
	""""Хранение настоек игры Alien Invasion"""
	
	def __init__(self):
		"""Инициализация настроек игры"""
		
		#Экран
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230, 230, 230)
		
		
		self.ship_limit = 3
		
		#Параметры пули
		self.bullet_speed_factor = 1
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullets_allowed = 3
		
		#Настройки пришельцев
		self.fleet_drop_speed = 20
		
		#Темп ускорения игры
		self.speedup_scale = 1.1
		#Темп прироста стоимости пришельцев
		self.score_scale = 1.5
		
		self.initialize_dynamic_settings()
		
	def initialize_dynamic_settings(self):
		"""Инициация настроек, меняющихся в ходе игры"""
		#Параметр скорости корабля
		self.ship_speed_factor = 1.5
		#Скорость пули
		self.bullet_width = 3
		#Скорость пришельцев
		self.alien_speed_factor = 1
		#fleet_direction: 1 - вправо, -1 - влево
		self.fleet_direction = 1
		#Подсчет очков
		self.alien_points = 50
		
	def increase_speed(self):
		"""Увеличивает настройки скорости"""
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		self.alien_points = int(self.alien_points * self.score_scale)
