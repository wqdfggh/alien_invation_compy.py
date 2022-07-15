
import sys
import pygame
from ai_settings import Settings
import game_function as gf
from ship import Ship
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
def run_game():
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
	pygame.display.set_caption("Alien Invation")
	play_button = Button(ai_settings, screen, "Play")
	ship = Ship(ai_settings, screen)
	bullets = Group()
	aliens = Group()
	
#	alien = Alien(ai_settings, screen)
	gf.create_fleet(ai_settings, screen, aliens, ship) 
	
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings, screen, stats)
	while True:
		
		gf.check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets, sb)
		if stats.game_active:
			ship.update()
			gf.bullets_update(ai_settings, screen, ship, bullets, aliens, stats, sb)
			gf.updata_aliens(ai_settings, stats, screen, ship, aliens, bullets, sb)
			
		gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button, sb)
 
run_game()
		
 
