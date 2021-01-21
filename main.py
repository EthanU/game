import pygame
from player import Player
from obstacle import Obstacle


hero = Player()

#array of all the non-player obstacles and static stuff on the screen
obstacles = []
obstacles.append(Obstacle('tree_1.png', 200, 300))
obstacles.append(Obstacle('tree_1.png', 700, 900))
obstacles.append(Obstacle('tree_1.png', 1200, 300))
obstacles.append(Obstacle('fence_1.png', 900, 700))
obstacles.append(Obstacle('fence_1.png', 100, 900))
obstacles.append(Obstacle('fence_1.png', 1000, 300))
obstacles.append(Obstacle('fence_1.png', 1050, 300))
obstacles.append(Obstacle('fence_1.png', 1000, 350))

pygame.init()
pygame.font.init()
#print(pygame.font.get_fonts())
font = pygame.font.SysFont('georgiabold', 30)

#make the window and name
window = pygame.display.set_mode((1600, 1000))
pygame.display.set_caption('NAME OF GAME')

def drawPlayer():
	window.blit(hero.image, (hero.x, hero.y))

def drawObstacles():
	for obs in obstacles:	
		window.blit(obs.image, (obs.x, obs.y))

def drawInventory():						#(x, y, width, height)
	if inventory_open:
		pygame.draw.rect(window, (255, 153, 51), (1000, 100, 600, 800))
		pygame.draw.rect(window, (200, 153, 51), (1050, 150, 500, 700))



def move(direction):
	
	collision = False

	#dont touch the math
	if direction == 'up':
		for obs in obstacles:
			if abs(hero.x - obs.x) < 40 and (hero.y - obs.y < 35) and (hero.y - obs.y > 0):
				collision = True;
		if not collision:
			for obs in obstacles:
				obs.y += hero.vel
	if direction == 'down':
		for obs in obstacles:
			if abs(hero.x - obs.x) < 40 and (obs.y - hero.y < 50) and (obs.y - hero.y > 0):
				collision = True;
		if not collision:
			for obs in obstacles:
				obs.y -= hero.vel
	if direction == 'left':
		for obs in obstacles:
			if hero.x - obs.x < 50 and hero.x - obs.x > 0 and (((hero.y - obs.y < 25) and (hero.y - obs.y > 0)) or (obs.y - hero.y < 45) and (obs.y - hero.y > 0)):
				collision = True;
		if not collision:
			for obs in obstacles:
				obs.x += hero.vel
	if direction == 'right':
		for obs in obstacles:
			if obs.x - hero.x < 50 and obs.x - hero.x > 0 and (((hero.y - obs.y < 25) and (hero.y - obs.y > 0)) or (obs.y - hero.y < 45) and (obs.y - hero.y > 0)):
				collision = True;
		if not collision:
			for obs in obstacles:
				obs.x -= hero.vel


inventory_open = False
inventory_open_delay = 0;

#update all time delays
def updateDelays():
	global inventory_open_delay
	if inventory_open_delay != 0:
		inventory_open_delay -= 1


#The main loop where the game runs
run = True
while run:
	pygame.time.delay(100)

	#specia events
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False


	#Key input
	keys = pygame.key.get_pressed()

	#directional input
	if keys[pygame.K_UP] and not inventory_open:
		move('up')
	if keys[pygame.K_DOWN] and not inventory_open:
		move('down')
	if keys[pygame.K_LEFT] and not inventory_open:
		move('left')
	if keys[pygame.K_RIGHT] and not inventory_open:
		move('right')

	#inventory input
	if keys[pygame.K_e]:
		if inventory_open_delay == 0:
			inventory_open = not inventory_open
			inventory_open_delay = 3
		
	#draw in all the stuff
	window.fill((0,0,0)) #fill background, deletes old positions of stuff
	
	drawObstacles()
	drawPlayer()
	drawInventory()
	updateDelays()

	pygame.display.update()

pygame.quit()




















