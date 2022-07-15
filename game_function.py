import pygame
import sys
from xia_bullet import Bullet
from alien import Alien
from time import sleep


def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets, sb):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit() 
		elif event.type == pygame.KEYDOWN:
			if stats.game_active:
				check_keydown_events(event, ai_settings, screen, ship, bullets)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
		elif  event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y, sb)
			
def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y, sb):
	
	
	if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active:
		
		ai_settings.initialize_dynamic_settings
		stats.reset_stats()
		
		stats.game_active = True
		aliens.empty()
		bullets.empty()
		sb.prep_score()
		create_fleet(ai_settings, screen, aliens, ship)
		ship.center_ship()
		
		pygame.mouse.set_visible(False)
		
def check_keyup_events(event, ship):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False
		
def check_keydown_events(event, ai_settings, screen, ship, bullets): 
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	if event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(ai_settings, screen, ship, bullets)
	elif event.key == pygame.K_q:
		sys.exit()


		
def fire_bullet(ai_settings, screen, ship, bullets):
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)
	
	
def bullets_update(ai_settings, screen, ship, bullets, aliens, stats, sb):
	bullets.update()
	
	for bullet in bullets.copy():
		if bullet.rect.bottom <=0:
			bullets.remove(bullet)
	check_bullet_alien_collisions(ai_settings, screen, ship, bullets, aliens, stats, sb)
	
def check_bullet_alien_collisions(ai_settings, screen, ship, bullets, aliens, stats ,sb):
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	if collisions:
		for aliens in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		check_high_score(stats, sb)
	if len(aliens) == 0:
		bullets.empty()
		ai_settings.increase_speed()
		stats.level += 1
		sb.prep_level()
		create_fleet(ai_settings, screen, aliens, ship)
		


			
def get_number_aliens_x(ai_settings, alien_width):
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2* alien_width))
	return number_aliens_x  
	
def get_number_rows(ai_settings, alien_height, ship_height):
	available_space_y = (ai_settings.screen_height -
							(3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows
def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
#	print(alien.x)
	alien.rect.x = alien.x
	
	
	alien_height = alien.rect.height
	alien.y = alien_height + 2 * alien_height * row_number
	alien.rect.y = alien.y

	
	aliens.add(alien)
	
	
	
	
def create_fleet(ai_settings, screen, aliens, ship):
	
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, alien.rect.height, ship.rect.height)
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			
			create_alien(ai_settings, screen, aliens, alien_number, row_number)


def updata_aliens(ai_settings, stats, screen, ship, aliens, bullets):
	check_fleet_edges(ai_settings, aliens)
	aliens.update()
	
	if pygame.sprite.spritecollideany(ship, aliens):
		print ("Ship hit!!!")
		ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
	check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)
		
def check_fleet_edges(ai_settings, aliens):
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break
def change_fleet_direction(ai_settings, aliens):
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

	


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
	
	if stats.ships_left >0:

		stats.ships_left -= 1
	
		aliens.empty()
		bullets.empty()
		
		create_fleet(ai_settings, screen, aliens, ship)
		ship.center_ship()
		sleep(0.5)
	else:
		
		stats.game_active = False
		pygame.mouse.set_visible(True)
		
		
def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
			break
	

def check_high_score(stats, sb):
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()
		
		
def update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button, sb):
	screen.fill(ai_settings.bg_color)
	ship.blitme()
	sb.show_score()
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	aliens.draw(screen)
	
	if not stats.game_active:
		play_button.draw_button()
	pygame.display.flip()
