import sys
import pygame
from settings import Settings
from ship import Ship
import game_functions as gf
from game_stats import GameStats
from pygame.sprite import Group
from button import Button
from scoreboard import Scoreboard

def run_game():
	
	#Создаем объект экрана
	pygame.init()
	
	#Получаем настройки
	ai_settings = Settings()
	
	screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion")
	
	#Создание статистики и очков
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings, screen, stats)
	
	#создание кнопки Play
	play_button = Button(ai_settings, screen, "Play")
	
	#Создание корабля
	ship = Ship(ai_settings, screen)
	
	#Создание группы для хранения пуль
	bullets = Group()
	
	#Создание группы для хранения пришельцев
	aliens = Group()
	#Создание флота пришельцев
	gf.create_fleet(ai_settings, screen, ship, aliens)
	
	#Цвет фона
	bg_color = (ai_settings.bg_color)
	
	#Создание пришельца
	# alien = Alien(ai_settings, screen)
	
	#Запуск основного цикла
	while True:
		#Отслеживание события клавиатуры и мыши
		gf.check_events(ai_settings, screen, stats, sb,
			play_button, ship, aliens, bullets)
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings, screen, stats, sb, ship, bullets, aliens)
			gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets)
		#Перерисовка экрана
		gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, 
				bullets, play_button)
		
run_game()
		
