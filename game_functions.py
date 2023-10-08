import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event, ai_settings, screen, ship, bullets):
	"""Нажатие клавиш"""
	if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
		#Перемещаем корабль вправо при зажатой кнопке
		ship.moving_right = True
	elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
		#Перемещаем корабль влево при зажатой кнопке
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		#Создание новой пули и включение ее группу bullets
		fire_bullet(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_q:
		sys.exit()

def check_keyup_events(event, ship):
	"""Отпускание клавиш"""
	#Останавливаем перемещение корабля при отпущенной кнопке
	if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
		#Останавливаем перемещение корабля при отпущенной кнопке
		ship.moving_left = False

def check_play_button(ai_settings, screen, stats, sb, play_button, 
		ship, aliens, bullets, mouse_x, mouse_y):
	"""Запускает новую игру при нажатии кнопки Play"""
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		#Скрываем указатель мыши
		pygame.mouse.set_visible(False)
		
		#Сбрасываем меняющиеся настройки
		ai_settings.initialize_dynamic_settings()
		
		#Сбор статистики
		stats.reset_stats()
		stats.game_active = True
		
		#Сброс счетов и уровня
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()
		
		#Очистка пуль и пришельцев
		aliens.empty()
		bullets.empty()
		
		#Содание нового флота и размещение корабля в центре
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
	#Отслеживание события клавиатуры и мыши
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, ship, bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, sb, play_button, 
				ship, aliens, bullets, mouse_x, mouse_y)
			

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
	"""Обновляет изображения на экране и отображает новый экран"""	
	#Перерисовка экрана
	screen.fill(ai_settings.bg_color)
	#Пули выводятся позади изображений корабля и пришельцев
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)
	#Вывод счета
	sb.show_score()
	#Кнопка Play отображается только при неактивной игре
	if not stats.game_active:
		play_button.draw_button()
	#Последний прорисованный экран
	pygame.display.flip()

def check_bullet_alien_collisions(ai_settings, screen, stats, sb,
		ship, aliens, bullets):
	"""Обработка коллизий пуль и пришельцев"""
	
	#Удаление пули и пришельца последними двумя параметрами
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
		sb.prep_score()
		check_high_score(stats, sb)
	# Проверка количества оставшихся пришельцев 
	#  реинкарнация флота, если текущий список пуст
	if len(aliens) == 0:
		bullets.empty()
		ai_settings.increase_speed()
		#Увеличение уровня
		stats.level += 1
		sb.prep_level()
		#Создание флота пришельцев
		create_fleet(ai_settings, screen, ship, aliens)

def update_bullets(ai_settings, screen, stats, sb, ship, bullets, aliens):
	"""Обновляет позиции пуль и уничтожает старые пули"""
	#Обновление позиции пули
	bullets.update()
	#Удаление старых пуль
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)
	# print(len(bullets))

def fire_bullet(ai_settings, screen, ship, bullets):
	"""Выпускает пулю, если не достигнут максимум их количества"""
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)

def get_number_aliens_x(ai_settings, alien_width):
	"""Вычисление количества пришельцев в ряду"""
	available_space_x = ai_settings.screen_width - (alien_width)
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	"""Создает пришельца и размещает его в ряду"""
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + (1.5 * alien_width * alien_number)
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
	"""создает флот пришельцев"""
	# Создание пришельца и вычисление количества пришельцев в ряду
	# Интервал между соседними пришельцами равен одной ширине пришельца
	alien = Alien(ai_settings, screen)	
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
	
	#Создание флота пришельцев
	for row_number in range(number_rows):
		#Создание превого пришельца
		for alien_number in range(number_aliens_x):
			#Создание пришельца и размещение его в ряду
			create_alien(ai_settings, screen, aliens, alien_number, row_number)

def get_number_rows(ai_settings, ship_height, alien_height):
	"""Определяет количество рядов, помещающихся на экране"""
	available_space_y = (ai_settings.screen_height - 
		(3* alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows

def check_fleet_edges(ai_settings, aliens):
	"""Реагирует на достижение пришельцем края экрана"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break

def change_fleet_direction(ai_settings, aliens):
	"""Опускает весь флот и меняет направление флота"""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1
	
def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
	"""Проверка контакта пришельцев с нинеим краем экрана"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
			break
	
def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
	""" Обновляет позиции всех пришельцев
		Проверяет достижение края экрана
	"""
	check_fleet_edges(ai_settings, aliens)
	aliens.update()
	
	#Коллизия пришелец-корабль
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
		
	#Проверка достижения нижнего края экрана
	check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)

def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
	"""Обработка столкновения корабля с пришельцами"""
	if stats.ships_left > 0:
		stats.ships_left -= 1
		sb.prep_ships()
	
		#Очитска пришельцев и пуль
		aliens.empty()
		bullets.empty()
	
		#Создание нового флота и размещение корабля в центре
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
	
		#Пауза
		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)
		
def check_high_score(stats, sb):
	"""проверяет появился ли новый рекорд"""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()
