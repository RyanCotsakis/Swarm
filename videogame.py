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

heroAccel = .3
heroRadius = 15

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
        pygame.draw.ellipse(screen, WHITE, [1 + self.x, self.y, 10, 10], 0)
     
        # Legs
        pygame.draw.line(screen, WHITE, [5 + self.x, 17 + self.y], [10 + self.x, 27 + self.y], 2)
        pygame.draw.line(screen, WHITE, [5 + self.x, 17 + self.y], [self.x, 27 + self.y], 2)
     
        # Body
        pygame.draw.line(screen, RED, [5 + self.x, 17 + self.y], [5 + self.x, 7 + self.y], 2)
     
        # Arms
        pygame.draw.line(screen, RED, [5 + self.x, 7 + self.y], [9 + self.x, 17 + self.y], 2)
        pygame.draw.line(screen, RED, [5 + self.x, 7 + self.y], [1 + self.x, 17 + self.y], 2)


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

    for i, bullet in enumerate(bullets):
        bullets[i].x += bullet.vx
        bullets[i].y += bullet.vy

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