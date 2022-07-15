import pygame

class Settings():
	def __init__(self):
		self.screen_width = 1200		
		self.screen_height = 800
		self.bg_color = (255, 255, 0)
		
		self.ship_speed = 5
		self.ship_limit = 2
		
		self.bullet_speed_factor = 2.5
		self.bullet_width = 300
		self.bullet_height = 15
		self.bullet_color = 60, 60, 60
		self.bullets_allowed = 5
		
		self.alien_speed_factor =1
		self.fleet_drop_speed = 10
		self.fleet_direction = 1
		
		self.speedup_scale = 1.1
		self.score_scale = 1.5
		
		self.initialize_dynamic_settings()
		
	def initialize_dynamic_settings(self):
		self.ship_speed = 1.5
		self.bullet_speed_factor = 3
		self.alien_speed_fator = 1
		
		self.fleet_direction = 1
		
		self.alien_points = 50
		
		
	
	def increase_speed(self):
		self.ship_speed *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		self.alien_points *= self.score_scale
		print(self.alien_points)
