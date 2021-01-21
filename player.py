import pygame

class Player(object):
	"""docstring for Player"""
	def __init__(self):
		super(Player, self).__init__()
		self.image = pygame.image.load('player.png')
		self.image = pygame.transform.scale(self.image, (50, 50))
		self.x = 775
		self.y = 475
		self.vel = 10
		