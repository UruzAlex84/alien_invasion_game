class GameStats():
	"""Отслеживание статистики игры Alien Invasion"""
	
	def __init__(self, ai_settings):
		"""Инициализация статистики"""
		self.ai_settings = ai_settings
		self.reset_stats()
		
		#Запуск игры в активном состоянии
		# self.game_active = True
		
		#Запуск игры в неактивном состоянии
		self.game_active = False
		
		#Рекорд не должен сбрасываться
		self.high_score = 0
	
	def reset_stats(self):
		"""Инициация статистики, меняющейся в ходе игры"""
		self.ships_left = self.ai_settings.ship_limit
		#Очки
		self.score = 0
		self.level = 1
