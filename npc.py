import pygame

class Npc(object):
	"""docstring for Npc"""
	def __init__(self, image_name, x, y, message):
		super(Npc, self).__init__()
		self.image = pygame.image.load(image_name)
		self.image = pygame.transform.scale(self.image, (50, 50))
		self.x = x
		self.y = y
		self.message = message
