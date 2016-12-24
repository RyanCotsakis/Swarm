import pygame
from random import randint

#GAME INITIATION

pygame.init()
screenSize = [1000,500]
screen = pygame.display.set_mode(screenSize)
 
pygame.display.set_caption("Swarm")

clock = pygame.time.Clock()

pygame.mouse.set_visible(0)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (127,127,127)
PINK = (255, 192, 203)

N = 0
E = 1
S = 2
W = 3

leftPress = False
rightPress = False
upPress = False
downPress = False
shootPress = False
blockerPress = False
missilePress = False

bullets = []
blockers = []
zombies = []
missiles = []
packages = []
zombieCount = 0
packageCount = 0
zombiesBetweenPackage = 10
timeBetweenZombies = 3000
timeBetweenPackages = timeBetweenZombies * zombiesBetweenPackage
zombieSpeed = 2

hudFont = pygame.font.SysFont("Courier New", 12)
titleFont = pygame.font.SysFont("Courier New", 20)

heroAccel = .5
heroRadius = 10
blockerWidth = 3*heroRadius
bulletSpeed = 5
missileSpeed = 5
blockerStrength = 100
missilesInPackage = 4
blockersInPackage = 8

#DEFINE OBJECTS

class Hero:
	def __init__(self, xPos, yPos, xVel, yVel, direction):
		self.x = xPos
		self.y = yPos
		self.vx = xVel
		self.vy = yVel
		self.direction = direction
		self.numOfBlockers = 0
		self.numOfMissiles = 0

	def shoot(self):
		if self.direction == N:
			newBullet = Bullet(self.x, self.y-heroRadius, self.vx, self.vy-bulletSpeed)
		elif self.direction == E:
			newBullet = Bullet(self.x+heroRadius, self.y, self.vx+bulletSpeed, self.vy)
		elif self.direction == S:
			newBullet = Bullet(self.x, self.y+heroRadius, self.vx, self.vy+bulletSpeed)
		else: #west
			newBullet = Bullet(self.x-heroRadius, self.y, self.vx-bulletSpeed, self.vy)

		for blocker in blockers:
			if blocker.contains(newBullet):
				return
		bullets.append(newBullet)


	def placeBlocker(self):
		newBlock = Blocker(self.x,self.y)
		for blocker in blockers:
			if newBlock.isAlready(blocker):
				return
		blockers.append(newBlock)
		self.numOfBlockers -= 1

	def draw(self):
		# Head
		pygame.draw.ellipse(screen, WHITE, [self.x-heroRadius, self.y-heroRadius, 2*heroRadius, 2*heroRadius], 0)

		if self.direction == N:
			# Eyes
			pygame.draw.ellipse(screen, RED, [self.x-9, self.y-7, 4, 4], 0)
			pygame.draw.ellipse(screen, RED, [self.x+5, self.y-7, 4, 4], 0)
		 
			# Arms
			pygame.draw.line(screen, RED, [self.x - 7, self.y - heroRadius], [self.x - 7, self.y - 3*heroRadius/2], 3)
			pygame.draw.line(screen, RED, [self.x + 7, self.y - heroRadius], [self.x + 7, self.y - 3*heroRadius/2], 3)

		elif self.direction == E:
			# Eyes
			pygame.draw.ellipse(screen, RED, [self.x+3, self.y-9, 4, 4], 0)
			pygame.draw.ellipse(screen, RED, [self.x+3, self.y+5, 4, 4], 0)
		 
			# Arms
			pygame.draw.line(screen, RED, [self.x + heroRadius, self.y - 7], [self.x + 3*heroRadius/2, self.y - 7], 3)
			pygame.draw.line(screen, RED, [self.x + heroRadius, self.y + 7], [self.x + 3*heroRadius/2, self.y + 7], 3)

		elif self.direction == S:
			# Eyes
			pygame.draw.ellipse(screen, RED, [self.x-9, self.y+3, 4, 4], 0)
			pygame.draw.ellipse(screen, RED, [self.x+5, self.y+3, 4, 4], 0)
		 
			# Arms
			pygame.draw.line(screen, RED, [self.x - 7, self.y + heroRadius], [self.x - 7, self.y + 3*heroRadius/2], 3)
			pygame.draw.line(screen, RED, [self.x + 7, self.y + heroRadius], [self.x + 7, self.y + 3*heroRadius/2], 3)

		elif self.direction == W:
			# Eyes
			pygame.draw.ellipse(screen, RED, [self.x-7, self.y-9, 4, 4], 0)
			pygame.draw.ellipse(screen, RED, [self.x-7, self.y+5, 4, 4], 0)
		 
			# Arms
			pygame.draw.line(screen, RED, [self.x - heroRadius, self.y - 7], [self.x - 3*heroRadius/2, self.y - 7], 3)
			pygame.draw.line(screen, RED, [self.x - heroRadius, self.y + 7], [self.x - 3*heroRadius/2, self.y + 7], 3)

class CarePackage:
	def __init__(self, xPos, yPos):
		self.x = xPos
		self.y = yPos
		self.isAlive = True

	def draw(self):
		pygame.draw.ellipse(screen, PINK, [self.x-5,self.y-5,11,11],3)

class Zombie:
	def __init__(self, hero, speed):
		self.speed = speed
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
		self.isAlive = True

	def move(self):
		vx = int(self.hero.x - self.x)
		vy = int(self.hero.y - self.y)
		avx = abs(vx)
		avy = abs(vy)
		self.vx = (self.speed*vx)/(avx+avy+1)
		self.vy = (self.speed*vy)/(avx+avy+1)
		self.x += self.vx
		self.y += self.vy
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
		self.isAlive = True

	def reflectX(self):
		self.vx = -self.vx
	
	def reflectY(self):
		self.vy = -self.vy

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

class Missile:
	def __init__(self, hero, direction):
		self.hero = hero
		self.direction = direction
		self.isAlive = True
		self.distance = heroRadius-missileSpeed
		self.move()

	def move(self):
		self.distance += missileSpeed
		if self.direction == N:
			self.x = self.hero.x
			self.y = self.hero.y - self.distance
		elif self.direction == E:
			self.x = self.hero.x + self.distance
			self.y = self.hero.y
		elif self.direction == S:
			self.x = self.hero.x
			self.y = self.hero.y + self.distance
		else:
			self.x = self.hero.x - self.distance
			self.y = self.hero.y

		if self.x <= 0 or self.x >= screenSize[0] or self.y <= 0 or self.y >= screenSize[1]:
			self.isAlive = False

	def draw(self):
		if self.direction == E or self.direction == W:
			pygame.draw.line(screen, WHITE, [self.x-4, self.y], [self.x+4, self.y], 3)
		else:
			pygame.draw.line(screen, WHITE, [self.x, self.y-4], [self.x, self.y+4], 3)

class Blocker:

	def __init__(self, xPos, yPos):
		self.x = xPos-xPos%(blockerWidth)
		self.y = yPos-yPos%(blockerWidth)
		self.health = blockerStrength
		self.isAlive = True

	def smash(self):
		self.health -= 1
		if self.health <= 0:
			self.isAlive = False

	def draw(self):
		pygame.draw.rect(screen, GREY, [self.x, self.y, blockerWidth-2, blockerWidth-2], 0)
		if self.health < blockerStrength/2:
			pygame.draw.line(screen, BLACK, [self.x, self.y], [self.x+blockerWidth, self.y + blockerWidth], 2)
		

	def isAlready(self, that):
		if self.x == that.x and self.y == that.y:
			return True
		return False

	def contains(self, that):
		if that.x >= self.x and that.x <= self.x+blockerWidth and that.y >= self.y and that.y <= self.y+blockerWidth:
			return True
		return False

	def relativeTo(self, that):
		if that.x < self.x:
			return E
		elif that.x > self.x + blockerWidth:
			return W
		elif that.y < self.y:
			return S
		elif that.y > self.y + blockerWidth:
			return N
		else:
			print "Error reading position relative to blocker"


#PLACE OBJECTS

hero = Hero(screenSize[0]/2,screenSize[1]/2,0,0,E)

#START GAME

gameOver = False
quit = False
while not gameOver:

	#EVENT LISTENING

	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			quit = True
 
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				leftPress = True
				hero.direction = W
				if shootPress:
					hero.shoot()
				if missilePress and hero.numOfMissiles > 0:
					missiles.append(Missile(hero,W))
					hero.numOfMissiles -= 1

			elif event.key == pygame.K_RIGHT:
				rightPress = True
				hero.direction = E
				if shootPress:
					hero.shoot()
				if missilePress and hero.numOfMissiles > 0:
					missiles.append(Missile(hero,E))
					hero.numOfMissiles -= 1

			elif event.key == pygame.K_UP:
				upPress = True
				hero.direction = N
				if shootPress:
					hero.shoot()
				if missilePress and hero.numOfMissiles > 0:
					missiles.append(Missile(hero,N))
					hero.numOfMissiles -= 1

			elif event.key == pygame.K_DOWN:
				downPress = True
				hero.direction = S
				if shootPress:
					hero.shoot()
				if missilePress and hero.numOfMissiles > 0:
					missiles.append(Missile(hero,S))
					hero.numOfMissiles -= 1

			elif event.key == pygame.K_a:
				missilePress = True

			elif event.key == pygame.K_s:
				shootPress = True

			elif event.key == pygame.K_d:
				blockerPress = True
 
		elif event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT:
				leftPress = False

			elif event.key == pygame.K_RIGHT:
				rightPress = False

			elif event.key == pygame.K_UP:
				upPress = False

			elif event.key == pygame.K_DOWN:
				downPress = False

			elif event.key == pygame.K_a:
				missilePress = False

			elif event.key == pygame.K_s:
				shootPress = False

			elif event.key == pygame.K_d:
				blockerPress = False

	if quit:
		break
		
	#MAKE CHANGES

	if blockerPress and hero.numOfBlockers >0:
		hero.placeBlocker()


	#move hero
	if not shootPress and not missilePress:
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

	#move missiles
	for missile in missiles:
		missile.move()

		for zombie in zombies:
			if abs(missile.x - zombie.x) <= heroRadius and abs(missile.y - zombie.y) <= heroRadius and missile.isAlive:
				missile.isAlive = False
				zombie.isAlive = False

	#pick up care packages
	for package in packages:
		if abs(package.x - hero.x) <= heroRadius and abs(package.y - hero.y) <= heroRadius:
			hero.numOfMissiles += missilesInPackage
			hero.numOfBlockers += blockersInPackage
			package.isAlive = False

	#move bullets
	for bullet in bullets:
		bullet.move()

		if abs(bullet.x - hero.x) <= heroRadius and abs(bullet.y - hero.y) <= heroRadius:
			gameOver = True

		for blocker in blockers:
			wasIn = False
			while blocker.contains(bullet):
				bullet.x -= bullet.vx
				bullet.y -= bullet.vy
				wasIn = True
			if wasIn:
				if blocker.relativeTo(bullet) == E or blocker.relativeTo(bullet) == W:
					bullet.reflectX()
				else:
					bullet.reflectY()

	#place care packages
	if pygame.time.get_ticks() > timeBetweenPackages * packageCount:
		packages.append(CarePackage(randint(0,screenSize[0]),randint(0,screenSize[1])))
		packageCount += 1

	#move zombies
	if pygame.time.get_ticks() > timeBetweenZombies * zombieCount:
		randomizer = randint(0,zombieCount/zombiesBetweenPackage)*randint(0,zombieCount/zombiesBetweenPackage) * 2 * zombiesBetweenPackage/(zombieCount+1)
		zombies.append(Zombie(hero,zombieSpeed+randomizer))
		zombieCount+=1

	for zombie in zombies:
		zombie.move()

		if abs(zombie.x - hero.x) <= 2*heroRadius and abs(zombie.y - hero.y) <= 2*heroRadius:
			gameOver = True

		for bullet in bullets:
			if abs(bullet.x - zombie.x) <= heroRadius and abs(bullet.y - zombie.y) <= heroRadius and bullet.isAlive:
				bullet.isAlive = False
				zombie.isAlive = False


		for blocker in blockers:
			while blocker.contains(zombie):
				blocker.smash()
				zombie.x -= zombie.vx
				zombie.y -= zombie.vy

	#DELETE STUFF

	for i, bullet in enumerate(bullets):
		if not bullet.isAlive:
			del bullets[i]

	for i, zombie in enumerate(zombies):
		if not zombie.isAlive:
			del zombies[i]

	for i, blocker in enumerate(blockers):
		if not blocker.isAlive:
			del blockers[i]

	for i, missile in enumerate(missiles):
		if not missile.isAlive:
			del missiles[i]

	for i, package in enumerate(packages):
		if not package.isAlive:
			del packages[i]

	#DRAW
	screen.fill(BLACK)

	for blocker in blockers:
		blocker.draw()

	for package in packages:
		package.draw()

	hero.draw()

	for zombie in zombies:
		zombie.draw()

	for missile in missiles:
		missile.draw()

	for bullet in bullets:
		bullet.draw()

	hud = hudFont.render("MISSILES: " + str(hero.numOfMissiles) + "  BLOCKERS: " + str(hero.numOfBlockers), False, WHITE)
	screen.blit(hud,(5,screenSize[1]-17))

	title = titleFont.render("LEVEL " + str(zombieCount/zombiesBetweenPackage + 1), False, WHITE)
	screen.blit(title,(screenSize[0]-120, 5))

	if gameOver:
		title = titleFont.render("GAME OVER", False, WHITE)
		screen.blit(title,(screenSize[0]/2-50, screenSize[1]/2-20))

	#UPDATE
	pygame.display.flip()
	clock.tick(20) #Limit frames per second

if gameOver:
	pygame.time.wait(2000)
pygame.quit()