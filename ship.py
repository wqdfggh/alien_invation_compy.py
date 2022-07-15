import pygame
from pygame.sprite import Sprite
class Ship(Sprite):
	
	def __init__(self, ai_settings, screen):
		super().__init__()
		self.ai_settings = ai_settings
		self.screen = screen
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom
		
		self.center = float(self.rect.centerx)
		
		self.moving_right = False
		self.moving_left = False
		
	def update(self):
		if self.rect.right < self.screen_rect.right and self.moving_right:
			self.center += self.ai_settings.ship_speed
		elif self.rect.left > self.screen_rect.left and self.moving_left:
			self.center -= self.ai_settings.ship_speed
		
		self.rect.centerx = self.center
	def blitme(self):
		self.screen.blit(self.image, self.rect)
	
	def center_ship(self):
		self.center = self.screen_rect.centerx
