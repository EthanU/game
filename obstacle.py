import pygame

class Obstacle(object):
	"""docstring for Obstacle"""
	def __init__(self, image_name, x, y):
		super(Obstacle, self).__init__()
		self.image = pygame.image.load(image_name).convert_alpha()
		self.image = pygame.transform.scale(self.image, (50, 50))
		self.x = x
		self.y = y
