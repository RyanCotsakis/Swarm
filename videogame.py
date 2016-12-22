import pygame


#GAME INITIATION

pygame.init()
screenSize = [1000,500]
screen = pygame.display.set_mode(screenSize)
 
pygame.display.set_caption("My Game")

clock = pygame.time.Clock()

pygame.mouse.set_visible(0)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (127,127,127)

N = 0
E = 1
S = 2
W = 3

leftPress = False
rightPress = False
upPress = False
downPress = False
shootPress = False

bullets = []
blockers = []

heroAccel = .5
heroRadius = 10

#DEFINE OBJECTS

class Hero:
	def __init__(self, xPos, yPos, xVel, yVel, direction):
		self.x = xPos
		self.y = yPos
		self.vx = xVel
		self.vy = yVel
		self.direction = direction

	def setPosition(self, x, y):
		self.x = x
		self.y = y

	def setVelocity(self, x, y):
		self.vx = x
		self.vy = y

	def shoot(self):
		bulletSpeed = 5
		if self.direction == N:
			bullets.append(Bullet(self.x, self.y-heroRadius, self.vx, self.vy-bulletSpeed))
		elif self.direction == E:
			bullets.append(Bullet(self.x+heroRadius, self.y, self.vx+bulletSpeed, self.vy))
		elif self.direction == S:
			bullets.append(Bullet(self.x, self.y+heroRadius, self.vx, self.vy+bulletSpeed))
		elif self.direction == W:
			bullets.append(Bullet(self.x-heroRadius, self.y, self.vx-bulletSpeed, self.vy))

	def placeBlocker(self):
		blockers.append(Blocker(self.x, self.y))

	def draw(self):
		# Head
		pygame.draw.ellipse(screen, WHITE, [self.x-heroRadius, self.y-heroRadius, 2*heroRadius, 2*heroRadius], 0)

		if self.direction == N:
			# Eyes
			pygame.draw.ellipse(screen, RED, [self.x-9, self.y-7, 4, 4], 0)
			pygame.draw.ellipse(screen, RED, [self.x+5, self.y-7, 4, 4], 0)
		 
			# Arms
			pygame.draw.line(screen, RED, [self.x - 7, self.y - heroRadius], [self.x - 7, self.y - 2*heroRadius], 3)
			pygame.draw.line(screen, RED, [self.x + 7, self.y - heroRadius], [self.x + 7, self.y - 2*heroRadius], 3)

		elif self.direction == E:
			# Eyes
			pygame.draw.ellipse(screen, RED, [self.x+3, self.y-9, 4, 4], 0)
			pygame.draw.ellipse(screen, RED, [self.x+3, self.y+5, 4, 4], 0)
		 
			# Arms
			pygame.draw.line(screen, RED, [self.x + heroRadius, self.y - 7], [self.x + 2*heroRadius, self.y - 7], 3)
			pygame.draw.line(screen, RED, [self.x + heroRadius, self.y + 7], [self.x + 2*heroRadius, self.y + 7], 3)

		elif self.direction == S:
			# Eyes
			pygame.draw.ellipse(screen, RED, [self.x-9, self.y+3, 4, 4], 0)
			pygame.draw.ellipse(screen, RED, [self.x+5, self.y+3, 4, 4], 0)
		 
			# Arms
			pygame.draw.line(screen, RED, [self.x - 7, self.y + heroRadius], [self.x - 7, self.y + 2*heroRadius], 3)
			pygame.draw.line(screen, RED, [self.x + 7, self.y + heroRadius], [self.x + 7, self.y + 2*heroRadius], 3)

		elif self.direction == W:
			# Eyes
			pygame.draw.ellipse(screen, RED, [self.x-7, self.y-9, 4, 4], 0)
			pygame.draw.ellipse(screen, RED, [self.x-7, self.y+5, 4, 4], 0)
		 
			# Arms
			pygame.draw.line(screen, RED, [self.x - heroRadius, self.y - 7], [self.x - 2*heroRadius, self.y - 7], 3)
			pygame.draw.line(screen, RED, [self.x - heroRadius, self.y + 7], [self.x - 2*heroRadius, self.y + 7], 3)


class Bullet:
	def __init__(self, xPos, yPos, xVel, yVel):
		self.x = xPos
		self.y = yPos
		self.vx = xVel
		self.vy = yVel
		self.health = 1
		self.isAlive = True

	def setPosition(self, x, y):
		self.x = x
		self.y = y

	def reflectX(self):
		self.vx = -self.vx
	
	def reflectY(self):
		self.vy = -self.vy

	def smash(self):
		self.health -= 1
		if self.health <= 0:
			self.isAlive = False

	def draw(self):
		pygame.draw.ellipse(screen, GREEN, [self.x, self.y, 5, 5], 0)


class Blocker:
	def __init__(self, xPos, yPos):
		self.x = xPos
		self.y = yPos
		self.health = 2
		self.isAlive = True

	def smash(self):
		self.health -= 1
		if self.health <= 0:
			self.isAlive = False

	def draw(self):
		pygame.draw.rect(screen, WHITE, [self.x, self.y, 10, 10], 0)

#PLACE OBJECTS

hero = Hero(0,0,0,0,E)

#START GAME

gameOver = False

while not gameOver:

	#EVENT LISTENING

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			gameOver = True
 
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				leftPress = True
				hero.direction = W
				if shootPress:
					hero.shoot()

			elif event.key == pygame.K_RIGHT:
				rightPress = True
				hero.direction = E
				if shootPress:
					hero.shoot()

			elif event.key == pygame.K_UP:
				upPress = True
				hero.direction = N
				if shootPress:
					hero.shoot()

			elif event.key == pygame.K_DOWN:
				downPress = True
				hero.direction = S
				if shootPress:
					hero.shoot()

			elif event.key == pygame.K_s:
				shootPress = True

			elif event.key == pygame.K_d:
				hero.placeBlocker()
 
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				leftPress = False

			elif event.key == pygame.K_RIGHT:
				rightPress = False

			elif event.key == pygame.K_UP:
				upPress = False

			elif event.key == pygame.K_DOWN:
				downPress = False

			elif event.key == pygame.K_s:
				shootPress = False
		
	#MAKE CHANGES
	if not shootPress:
		if leftPress:
			hero.vx -= heroAccel
		if rightPress:
			hero.vx += heroAccel
		if upPress:
			hero.vy -= heroAccel
		if downPress:
			hero.vy += heroAccel  
	hero.x += hero.vx
	hero.y += hero.vy

	if hero.x <= 0:
		hero.x = 1
		hero.vx = 0
	if hero.y <= 0:
		hero.y = 1
		hero.vy = 0
	if hero.x >= screenSize[0]:
		hero.x = screenSize[0]-1
		hero.vx = 0
	if hero.y > screenSize[1]:
		hero.y = screenSize[1]-1
		hero.vy = 0

	for i, bullet in enumerate(bullets):
		bullets[i].x += bullet.vx
		bullets[i].y += bullet.vy

		if bullet.x <= 0:
			bullets[i].reflectX()
			bullets[i].x = 1
		if bullet.x >= screenSize[0]:
			bullets[i].reflectX()
			bullets[i].x = screenSize[0]-1
		if bullet.y <= 0:
			bullets[i].reflectY()
			bullets[i].y = 1
		if bullet.y >= screenSize[1]:
			bullets[i].reflectY()
			bullets[i].y = screenSize[1]-1

		if abs(bullet.x - hero.x) <= heroRadius and abs(bullet.y - hero.y) <= heroRadius:
			del bullets[i]

	#DRAW
	screen.fill(BLACK)

	hero.draw()
	for bullet in bullets:
		bullet.draw()
	for blocker in blockers:
		blocker.draw()
	#draw stuff here (after screen.fill)
 
	#UPDATE
	pygame.display.flip()
	clock.tick(20) #Limit frames per second

pygame.quit()