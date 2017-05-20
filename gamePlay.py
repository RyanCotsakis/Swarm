import pygame
from random import randint
import time

#COMMON VARIABLES
screenSize = [1100,550]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255,128,0)
GREY = (127,127,127)
PINK = (255, 192, 203)
BLUE = (0,0,255)

SENTINEL = -100

N = 0
E = 1
S = 2
W = 3
zombiesBetweenPackage = 10
timeBetweenZombies = 3000
timeBetweenPackages = timeBetweenZombies * zombiesBetweenPackage
zombieSpeed = 2
readyForLevel = True

heroRadius = 10
heroAccel = .5
blockerWidth = 3*heroRadius
bulletSpeed = 5
missileSpeed = 5
blockerStrength = 100
missilesInPackage = 4
blockersInPackage = 8
bulletHealth = 5

BULLET = 0
BLOCKER = 1
ZOMBIE = 2
MISSILE = 3
PACKAGE = 4
HERO = 5


class ObjectList:
	def __init__(self):
		self.bullets = []
		self.blockers = []
		self.zombies = []
		self.missiles = []
		self.packages = []
		self.heros = []

	def find_id(self, type_id, screen):
		typ = int(type_id[0])
		id = int(type_id[1:])
		for bullet in self.bullets:
			if bullet.id == id:
				return bullet
		for blocker in self.blockers:
			if blocker.id == id:
				return blocker
		for zombie in self.zombies:
			if zombie.id == id:
				return zombie
		for missile in self.missiles:
			if missile.id == id:
				return missile
		for package in self.packages:
			if package.id == id:
				return package
		for hero in self.heros:
			if hero.id == id:
				return hero
		#make a new instance of type "typ"
		if typ == BULLET:
			newBullet = Bullet(int(id), screen, 0,0,0,0) #self, id, screen, xPos, yPos, xVel, yVel
			self.bullets.append(newBullet)
			return newBullet
		elif typ == BLOCKER:
			newBlocker = Blocker(int(id), screen, 0,0) #self, id, screen, xPos, yPos
			self.blockers.append(newBlocker)
			return newBlocker
		elif typ == ZOMBIE:
			newZombie = Zombie(int(id), screen, self.heros, 0,0,0) #self, id, screen, heros, speed, smart, strong
			self.zombies.append(newZombie)
			return newZombie
		elif typ == MISSILE:
			#self, id, screen, hero, direction
			newMissile = Missile(int(id), screen, self.heros[0],0)
			self.missiles.append(newMissile)
			return newMissile
		elif typ == PACKAGE:
			#self, id, screen, xPos, yPos
			newPackage = CarePackage(int(id), screen, 0,0)
			self.packages.append(newPackage)
			return newPackage
		elif typ == HERO:
			#self, id, screen, xPos, yPos, xVel, yVel, direction, client
			newHero = Hero(int(id), screen, 0,0,0,0,0,0)
			self.heros.append(newHero)
			return newHero
			
		raise Exception("Could not find id: " + str(type_id))

	def handle_command(self, command_string, screen):
		#1(typ)5(id)rest(args)
		id = command_string[:6]
		args = command_string[6:]
		self.find_id(id, screen).command(args)


objs = ObjectList()

class Identifier:
	def __init__(self):
		self.n = 0

	def next(self):
		self.n += 1
		return self.n
		
ii = Identifier()

class Stopwatch:
	def __init__(self):
		self.startTime = pygame.time.get_ticks()
		self.lastPause = self.startTime
		self.paused = False
	def getTime(self):
		return pygame.time.get_ticks() - self.startTime
	def pause(self):
		self.lastPause = pygame.time.get_ticks()
		self.paused = True
	def play(self):
		if self.paused:
			self.startTime += pygame.time.get_ticks() - self.lastPause
		self.paused = False
	def wait(self, dur):
		self.startTime += 1000*dur

class Hero:
	def __init__(self, id, screen, xPos, yPos, xVel, yVel, direction, client):
		self.id = id
		self.x = xPos
		self.y = yPos
		self.vx = xVel
		self.vy = yVel
		self.direction = direction
		self.numOfBlockers = 0
		self.numOfMissiles = 0
		self.screen = screen
		self.client = client

		self.leftPress = False
		self.rightPress = False
		self.upPress = False
		self.downPress = False
		self.shootPress = False
		self.blockerPress = False
		self.missilePress = False

		self.isAlive = True

	def shoot(self):
		if self.direction == N:
			newBullet = Bullet(ii.next(), self.screen, self.x, self.y-heroRadius, self.vx, self.vy-bulletSpeed)
		elif self.direction == E:
			newBullet = Bullet(ii.next(), self.screen, self.x+heroRadius, self.y, self.vx+bulletSpeed, self.vy)
		elif self.direction == S:
			newBullet = Bullet(ii.next(), self.screen, self.x, self.y+heroRadius, self.vx, self.vy+bulletSpeed)
		else: #west
			newBullet = Bullet(ii.next(), self.screen, self.x-heroRadius, self.y, self.vx-bulletSpeed, self.vy)

		for blocker in objs.blockers:
			if blocker.contains(newBullet):
				return
		objs.bullets.append(newBullet)


	def placeBlocker(self):
		newBlock = Blocker(ii.next(), self.screen, self.x,self.y)
		for blocker in objs.blockers:
			if newBlock.isAlready(blocker):
				return
		for bullet in objs.bullets:
			if newBlock.contains(bullet):
				return
		objs.blockers.append(newBlock)
		self.numOfBlockers -= 1

	def command(self, args):
		self.x = int(args[0:4])
		self.y = int(args[4:8])
		self.direction = int(args[8])
		self.isAlive = int(args[9])

	def draw(self):
		# Head
		pygame.draw.ellipse(self.screen, WHITE, [self.x-heroRadius, self.y-heroRadius, 2*heroRadius, 2*heroRadius], 0)

		if self.direction == N:
			# Eyes
			pygame.draw.ellipse(self.screen, RED, [self.x-9, self.y-7, 4, 4], 0)
			pygame.draw.ellipse(self.screen, RED, [self.x+5, self.y-7, 4, 4], 0)
		 
			# Arms
			pygame.draw.line(self.screen, RED, [self.x - 7, self.y - heroRadius], [self.x - 7, self.y - 3*heroRadius/2], 3)
			pygame.draw.line(self.screen, RED, [self.x + 7, self.y - heroRadius], [self.x + 7, self.y - 3*heroRadius/2], 3)

		elif self.direction == E:
			# Eyes
			pygame.draw.ellipse(self.screen, RED, [self.x+3, self.y-9, 4, 4], 0)
			pygame.draw.ellipse(self.screen, RED, [self.x+3, self.y+5, 4, 4], 0)
		 
			# Arms
			pygame.draw.line(self.screen, RED, [self.x + heroRadius, self.y - 7], [self.x + 3*heroRadius/2, self.y - 7], 3)
			pygame.draw.line(self.screen, RED, [self.x + heroRadius, self.y + 7], [self.x + 3*heroRadius/2, self.y + 7], 3)

		elif self.direction == S:
			# Eyes
			pygame.draw.ellipse(self.screen, RED, [self.x-9, self.y+3, 4, 4], 0)
			pygame.draw.ellipse(self.screen, RED, [self.x+5, self.y+3, 4, 4], 0)
		 
			# Arms
			pygame.draw.line(self.screen, RED, [self.x - 7, self.y + heroRadius], [self.x - 7, self.y + 3*heroRadius/2], 3)
			pygame.draw.line(self.screen, RED, [self.x + 7, self.y + heroRadius], [self.x + 7, self.y + 3*heroRadius/2], 3)

		elif self.direction == W:
			# Eyes
			pygame.draw.ellipse(self.screen, RED, [self.x-7, self.y-9, 4, 4], 0)
			pygame.draw.ellipse(self.screen, RED, [self.x-7, self.y+5, 4, 4], 0)
		 
			# Arms
			pygame.draw.line(self.screen, RED, [self.x - heroRadius, self.y - 7], [self.x - 3*heroRadius/2, self.y - 7], 3)
			pygame.draw.line(self.screen, RED, [self.x - heroRadius, self.y + 7], [self.x - 3*heroRadius/2, self.y + 7], 3)

class CarePackage:
	def __init__(self, id, screen, xPos, yPos):
		self.id = id
		self.x = xPos
		self.y = yPos
		self.isAlive = True
		self.screen = screen

	def command(self, args):
		self.x = int(args[0:4])
		self.y = int(args[4:8])
		self.isAlive = int(args[8])

	def draw(self):
		pygame.draw.ellipse(self.screen, PINK, [self.x-6,self.y-6,13,13],3)

class Zombie:
	def __init__(self, id, screen, heros, speed, smart, strong):
		self.id = id
		self.vx = 0
		self.vy = 0
		if not strong:
			self.speed = speed
		else:
			self.speed = zombieSpeed
		self.smart = smart
		self.screen = screen
		self.strong = strong
		
		if self.smart:
			self.smartness = randint(0,255)
		else:
			self.smartness = 0
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
		self.direction = (side+2)%4
		self.isAlive = True

	def distanceTo2(self, hero):
		return (self.x-hero.x)*(self.x-hero.x) + (self.y-hero.y)*(self.y-hero.y)

	def move(self):
		min, closestHero = self.distanceTo2(objs.heros[0]), objs.heros[0]
		for hero in objs.heros:
			if self.distanceTo2(hero) < min:
				min, closestHero = self.distanceTo2(hero), hero
		vx = int(closestHero.x - self.x)
		vy = int(closestHero.y - self.y)

		#Smart zombies avoid bullets
		if self.smart:
			for bullet in objs.bullets:
				bvx = bullet.vx
				bvy = bullet.vy
				rx = self.x-bullet.x
				ry = self.y-bullet.y
				dot = (bvx*rx+bvy*ry)
				if dot > 0:
					distToPathx = (rx-bvx*dot/(bvx*bvx+bvy*bvy+1))
					distToPathy = (ry-bvy*dot/(bvx*bvx+bvy*bvy+1))
					distToPath2 = distToPathx*distToPathx+distToPathy*distToPathy
					if not distToPathx or not distToPathy:
						vx = 100
						vy = 100
					else:
						danger = self.smartness*(abs(vx)+abs(vy))/(abs(rx)+abs(ry))/distToPath2
						vx += danger*distToPathx
						vy += danger*distToPathy


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

	def command(self, args):
		self.x = int(args[0:4])
		self.y = int(args[4:8])
		self.direction = int(args[8])
		self.strong = int(args[9])
		self.smartness = int(args[10:14])
		self.smart = self.smartness
		self.isAlive = int(args[14])

	def draw(self):
		# Head
		if self.smart:
			color = (255*(1-self.strong), self.smartness, 255*self.strong)
		else:
			color = (255*(1-self.strong), 0, 255*self.strong)
		pygame.draw.ellipse(self.screen, color, [self.x-heroRadius, self.y-heroRadius, 2*heroRadius, 2*heroRadius], 0)

		if self.direction == N:
			# Eyes
			pygame.draw.ellipse(self.screen, GREEN, [self.x-9, self.y-7, 4, 4], 0)
			pygame.draw.ellipse(self.screen, GREEN, [self.x+5, self.y-7, 4, 4], 0)
		 
			# Arms
			pygame.draw.line(self.screen, GREEN, [self.x - 7, self.y - heroRadius], [self.x - 7, self.y - 2*heroRadius], 3)
			pygame.draw.line(self.screen, GREEN, [self.x + 7, self.y - heroRadius], [self.x + 7, self.y - 2*heroRadius], 3)

		elif self.direction == E:
			# Eyes
			pygame.draw.ellipse(self.screen, GREEN, [self.x+3, self.y-9, 4, 4], 0)
			pygame.draw.ellipse(self.screen, GREEN, [self.x+3, self.y+5, 4, 4], 0)
		 
			# Arms
			pygame.draw.line(self.screen, GREEN, [self.x + heroRadius, self.y - 7], [self.x + 2*heroRadius, self.y - 7], 3)
			pygame.draw.line(self.screen, GREEN, [self.x + heroRadius, self.y + 7], [self.x + 2*heroRadius, self.y + 7], 3)

		elif self.direction == S:
			# Eyes
			pygame.draw.ellipse(self.screen, GREEN, [self.x-9, self.y+3, 4, 4], 0)
			pygame.draw.ellipse(self.screen, GREEN, [self.x+5, self.y+3, 4, 4], 0)
		 
			# Arms
			pygame.draw.line(self.screen, GREEN, [self.x - 7, self.y + heroRadius], [self.x - 7, self.y + 2*heroRadius], 3)
			pygame.draw.line(self.screen, GREEN, [self.x + 7, self.y + heroRadius], [self.x + 7, self.y + 2*heroRadius], 3)

		elif self.direction == W:
			# Eyes
			pygame.draw.ellipse(self.screen, GREEN, [self.x-7, self.y-9, 4, 4], 0)
			pygame.draw.ellipse(self.screen, GREEN, [self.x-7, self.y+5, 4, 4], 0)
		 
			# Arms
			pygame.draw.line(self.screen, GREEN, [self.x - heroRadius, self.y - 7], [self.x - 2*heroRadius, self.y - 7], 3)
			pygame.draw.line(self.screen, GREEN, [self.x - heroRadius, self.y + 7], [self.x - 2*heroRadius, self.y + 7], 3)

class Bullet:
	def __init__(self, id, screen, xPos, yPos, xVel, yVel):
		self.id = id
		self.x = xPos
		self.y = yPos
		self.vx = xVel
		self.vy = yVel
		self.screen = screen
		self.isAlive = True
		self.health = bulletHealth + randint(0,3) + randint(0,3)

	def reflectX(self):
		self.health -= 1
		if self.health == 1:
			self.vx = -int(self.vx/2)
		else:
			self.vx = -self.vx
		if self.health <= 0:
			self.isAlive = False
	
	def reflectY(self):
		self.health -= 1
		if self.health == 1:
			self.vy = -int(self.vy/2)
		else:
			self.vy = -self.vy
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

	def command(self, args):
		self.x = int(args[0:4])
		self.y = int(args[4:8])
		self.health = int(args[8:10])
		self.isAlive = int(args[10])

	def draw(self):
		if self.health == 1:
			color = (0,128,0)
		elif self.health == 2:
			color = (0,255,0)
		else:
			color = (0,255,128)
		pygame.draw.ellipse(self.screen, color, [self.x, self.y, 5, 5], 0)

class Missile:
	def __init__(self, id, screen, hero, direction):
		self.id = id
		self.hero = hero
		self.direction = direction
		self.isAlive = True
		self.distance = heroRadius-missileSpeed
		self.screen = screen
		self.move() #so the hero is not instantly killed

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

	def command(self, args):
		self.x = int(args[0:4])
		self.y = int(args[4:8])
		self.direction = int(args[8])
		self.isAlive = int(args[9])

	def draw(self):
		if self.direction == E or self.direction == W:
			pygame.draw.line(self.screen, WHITE, [self.x-4, self.y], [self.x+4, self.y], 3)
		else:
			pygame.draw.line(self.screen, WHITE, [self.x, self.y-4], [self.x, self.y+4], 3)

class Blocker:

	def __init__(self, id, screen, xPos, yPos):
		self.id = id
		self.x = xPos-xPos%(blockerWidth)
		self.y = yPos-yPos%(blockerWidth)
		self.health = blockerStrength
		self.isAlive = True
		self.screen = screen

	def smash(self):
		self.health -= 1
		if self.health <= 0:
			self.isAlive = False		

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

	def command(self, args):
		self.x = int(args[0:4])
		self.y = int(args[4:8])
		self.health = int(args[8:12])
		self.isAlive = int(args[12])

	def draw(self):
		pygame.draw.rect(self.screen, GREY, [self.x, self.y, blockerWidth-2, blockerWidth-2], 0)
		if self.health < blockerStrength/2:
			pygame.draw.line(self.screen, BLACK, [self.x, self.y], [self.x+blockerWidth, self.y + blockerWidth], 2)