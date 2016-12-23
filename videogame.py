import pygame
from random import randint

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
zombies = []
zombieCount = 0
timeBetweenZombies = 3000
zombieSpeed = 4

heroAccel = .5
heroRadius = 10
mapSize = [200*heroRadius,100*heroRadius] #todo: implement this

#DEFINE OBJECTS

class Hero:
	def __init__(self, xPos, yPos, xVel, yVel, direction):
		self.x = xPos
		self.y = yPos
		self.vx = xVel
		self.vy = yVel
		self.direction = direction

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
		newBlock = Blocker(self.x,self.y)
		for blocker in blockers:
			if newBlock.isOn(blocker):
				return
		blockers.append(newBlock)

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

class Zombie:
	def __init__(self, hero):
		side = randint(0,3)
		if side == N:
			self.x = randint(0,screenSize[0])
			self.y = -heroRadius
		elif side == E:
			self.y = randint(0,screenSize[1])
			self.x = screenSize[0]+heroRadius
		elif side == S:
			self.x = randint(0,screenSize[0])
			self.y = screenSize[1]+heroRadius
		elif side == W:
			self.y = randint(0,screenSize[1])
			self.x = -heroRadius
		self.hero = hero
		self.direction = (side+2)%4

	def move(self):
		vx = int(self.hero.x - self.x)
		vy = int(self.hero.y - self.y)
		avx = abs(vx)
		avy = abs(vy)
		self.x += (zombieSpeed*vx)/(avx+avy+1)
		self.y += (zombieSpeed*vy)/(avx+avy+1)
		if avy > avx and vy > vx:
			self.direction = S
		if avx > avy and vx > vy:
			self.direction = E
		if avy > avx and vy < vx:
			self.direction = N
		if avx > avy and vx < vy:
			self.direction = W


	def draw(self):
		# Head
		pygame.draw.ellipse(screen, RED, [self.x-heroRadius, self.y-heroRadius, 2*heroRadius, 2*heroRadius], 0)

		if self.direction == N:
			# Eyes
			pygame.draw.ellipse(screen, GREEN, [self.x-9, self.y-7, 4, 4], 0)
			pygame.draw.ellipse(screen, GREEN, [self.x+5, self.y-7, 4, 4], 0)
		 
			# Arms
			pygame.draw.line(screen, GREEN, [self.x - 7, self.y - heroRadius], [self.x - 7, self.y - 2*heroRadius], 3)
			pygame.draw.line(screen, GREEN, [self.x + 7, self.y - heroRadius], [self.x + 7, self.y - 2*heroRadius], 3)

		elif self.direction == E:
			# Eyes
			pygame.draw.ellipse(screen, GREEN, [self.x+3, self.y-9, 4, 4], 0)
			pygame.draw.ellipse(screen, GREEN, [self.x+3, self.y+5, 4, 4], 0)
		 
			# Arms
			pygame.draw.line(screen, GREEN, [self.x + heroRadius, self.y - 7], [self.x + 2*heroRadius, self.y - 7], 3)
			pygame.draw.line(screen, GREEN, [self.x + heroRadius, self.y + 7], [self.x + 2*heroRadius, self.y + 7], 3)

		elif self.direction == S:
			# Eyes
			pygame.draw.ellipse(screen, GREEN, [self.x-9, self.y+3, 4, 4], 0)
			pygame.draw.ellipse(screen, GREEN, [self.x+5, self.y+3, 4, 4], 0)
		 
			# Arms
			pygame.draw.line(screen, GREEN, [self.x - 7, self.y + heroRadius], [self.x - 7, self.y + 2*heroRadius], 3)
			pygame.draw.line(screen, GREEN, [self.x + 7, self.y + heroRadius], [self.x + 7, self.y + 2*heroRadius], 3)

		elif self.direction == W:
			# Eyes
			pygame.draw.ellipse(screen, GREEN, [self.x-7, self.y-9, 4, 4], 0)
			pygame.draw.ellipse(screen, GREEN, [self.x-7, self.y+5, 4, 4], 0)
		 
			# Arms
			pygame.draw.line(screen, GREEN, [self.x - heroRadius, self.y - 7], [self.x - 2*heroRadius, self.y - 7], 3)
			pygame.draw.line(screen, GREEN, [self.x - heroRadius, self.y + 7], [self.x - 2*heroRadius, self.y + 7], 3)

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

	def move(self):
		self.x += self.vx
		self.y += self.vy

		if self.x <= 0:
			self.reflectX()
			self.x = 1
		if self.x >= screenSize[0]:
			self.reflectX()
			self.x = screenSize[0]-1
		if self.y <= 0:
			self.reflectY()
			self.y = 1
		if self.y >= screenSize[1]:
			self.reflectY()
			self.y = screenSize[1]-1

	def draw(self):
		pygame.draw.ellipse(screen, GREEN, [self.x, self.y, 5, 5], 0)


class Blocker:
	def __init__(self, xPos, yPos):
		self.x = xPos-xPos%(3*heroRadius)
		self.y = yPos-yPos%(3*heroRadius)
		self.health = 2
		self.isAlive = True

	def smash(self):
		self.health -= 1
		if self.health <= 0:
			self.isAlive = False

	def draw(self):
		pygame.draw.rect(screen, GREY, [self.x, self.y, 3*heroRadius-2, 3*heroRadius-2], 0)

	def isOn(self, that):
		if self.x == that.x and self.y == that.y:
			return True


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

	#move hero
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
	if hero.y >= screenSize[1]:
		hero.y = screenSize[1]-1
		hero.vy = 0

	#move bullets
	for i, bullet in enumerate(bullets):
		bullets[i].move()

		if abs(bullet.x - hero.x) <= heroRadius and abs(bullet.y - hero.y) <= heroRadius:
			del bullets[i]
			gameOver = True

	#move zombies
	if not pygame.time.get_ticks() < timeBetweenZombies * zombieCount:
		zombies.append(Zombie(hero))
		zombieCount+=1 

	for i, zombie in enumerate(zombies):
		zombies[i].move()

		if abs(zombie.x - hero.x) <= 2*heroRadius and abs(zombie.y - hero.y) <= 2*heroRadius:
			del zombies[i]
			gameOver = True

		for j, bullet in enumerate(bullets):
			if abs(bullet.x - zombie.x) <= heroRadius and abs(bullet.y - zombie.y) <= heroRadius:
				del bullets[j]
				del zombies[i]

	#DRAW
	screen.fill(BLACK)

	for blocker in blockers:
		blocker.draw()

	hero.draw()

	for zombie in zombies:
		zombie.draw()

	for bullet in bullets:
		bullet.draw()
 
	#UPDATE
	pygame.display.flip()
	clock.tick(20) #Limit frames per second

pygame.quit()