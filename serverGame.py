from gamePlay import *
import sys

def start(clients):

	pygame.init()
	screen = pygame.display.set_mode(screenSize)
	 
	pygame.display.set_caption("Swarm")

	clock = pygame.time.Clock()
	pygame.mouse.set_visible(0)

	hudFont = pygame.font.SysFont("Courier New", 12)
	titleFont = pygame.font.SysFont("Courier New", 20)

	zombiesBetweenPackage = 10
	timeBetweenZombies = 3000
	timeBetweenPackages = timeBetweenZombies * zombiesBetweenPackage
	zombieSpeed = 2
	readyForLevel = True

	for client in clients:
		client.send("_START")

	quit = False
	while not quit:

		zombieCount = 0
		packageCount = 0
		stopwatch = Stopwatch()

		hero = Hero(ii.next(), screen, screenSize[0]/2,screenSize[1]/2,0,0,E,SENTINEL)
		objs.heros.append(hero)
		i = 1
		for client in clients:
			objs.heros.append(Hero(ii.next(), screen, screenSize[0]/2,screenSize[1]/2,0,0,E,client))
			client.send("_INDEX: " + str(i))
			i += 1

		for thehero in objs.heros:
			thehero.numOfBlockers = 0
			thehero.numOfMissiles = 0

		sendAdditionalInfo = 0

		gameOver = False
		while not gameOver:

			#EVENT LISTENING

			for event in pygame.event.get():

				if event.type == pygame.QUIT:
					quit = True
		 
				elif event.type == pygame.KEYDOWN:
					if not stopwatch.paused:
						if event.key == pygame.K_LEFT:
							hero.leftPress = True
							hero.direction = W
							if hero.shootPress:
								hero.shoot()
							if hero.missilePress and hero.numOfMissiles > 0:
								objs.missiles.append(Missile(ii.next(), screen, hero,W))
								hero.numOfMissiles -= 1

						elif event.key == pygame.K_RIGHT:
							hero.rightPress = True
							hero.direction = E
							if hero.shootPress:
								hero.shoot()
							if hero.missilePress and hero.numOfMissiles > 0:
								objs.missiles.append(Missile(ii.next(), screen, hero,E))
								hero.numOfMissiles -= 1

						elif event.key == pygame.K_UP:
							hero.upPress = True
							hero.direction = N
							if hero.shootPress:
								hero.shoot()
							if hero.missilePress and hero.numOfMissiles > 0:
								objs.missiles.append(Missile(ii.next(), screen,hero,N))
								hero.numOfMissiles -= 1

						elif event.key == pygame.K_DOWN:
							hero.downPress = True
							hero.direction = S
							if hero.shootPress:
								hero.shoot()
							if hero.missilePress and hero.numOfMissiles > 0:
								objs.missiles.append(Missile(ii.next(), screen,hero,S))
								hero.numOfMissiles -= 1

					if event.key == pygame.K_a:
						hero.missilePress = True

					elif event.key == pygame.K_s:
						hero.shootPress = True

					elif event.key == pygame.K_d:
						hero.blockerPress = True

					elif event.key == pygame.K_p:
						if not stopwatch.paused:
							stopwatch.pause()
						else:
							stopwatch.play()
		 
				elif event.type == pygame.KEYUP:
					if event.key == pygame.K_LEFT:
						hero.leftPress = False

					elif event.key == pygame.K_RIGHT:
						hero.rightPress = False

					elif event.key == pygame.K_UP:
						hero.upPress = False

					elif event.key == pygame.K_DOWN:
						hero.downPress = False

					elif event.key == pygame.K_a:
						hero.missilePress = False

					elif event.key == pygame.K_s:
						hero.shootPress = False

					elif event.key == pygame.K_d:
						hero.blockerPress = False

			if quit:
				break
			
	
			#LISTEN TO SERVER
			for thehero in objs.heros:
				if thehero.client != SENTINEL:
					for event in thehero.client.get():
						down = int(event[0])
						key = int(event[1:])
				 
						if down:
							if not stopwatch.paused:
								if key == pygame.K_LEFT:
									thehero.leftPress = True
									thehero.direction = W
									if thehero.shootPress:
										thehero.shoot()
									if thehero.missilePress and thehero.numOfMissiles > 0:
										objs.missiles.append(Missile(ii.next(), screen, thehero,W))
										thehero.numOfMissiles -= 1

								elif key == pygame.K_RIGHT:
									thehero.rightPress = True
									thehero.direction = E
									if thehero.shootPress:
										thehero.shoot()
									if thehero.missilePress and thehero.numOfMissiles > 0:
										objs.missiles.append(Missile(ii.next(), screen, thehero,E))
										thehero.numOfMissiles -= 1

								elif key == pygame.K_UP:
									thehero.upPress = True
									thehero.direction = N
									if thehero.shootPress:
										thehero.shoot()
									if thehero.missilePress and thehero.numOfMissiles > 0:
										objs.missiles.append(Missile(ii.next(), screen, thehero,N))
										thehero.numOfMissiles -= 1

								elif key == pygame.K_DOWN:
									thehero.downPress = True
									thehero.direction = S
									if thehero.shootPress:
										thehero.shoot()
									if thehero.missilePress and thehero.numOfMissiles > 0:
										objs.missiles.append(Missile(ii.next(), screen,thehero,S))
										thehero.numOfMissiles -= 1

							if key == pygame.K_a:
								thehero.missilePress = True

							elif key == pygame.K_s:
								thehero.shootPress = True

							elif key == pygame.K_d:
								thehero.blockerPress = True
				 
						else:
							if key == pygame.K_LEFT:
								thehero.leftPress = False

							elif key == pygame.K_RIGHT:
								thehero.rightPress = False

							elif key == pygame.K_UP:
								thehero.upPress = False

							elif key == pygame.K_DOWN:
								thehero.downPress = False

							elif key == pygame.K_a:
								thehero.missilePress = False

							elif key == pygame.K_s:
								thehero.shootPress = False

							elif key == pygame.K_d:
								thehero.blockerPress = False



			#MAKE CHANGES
			if not stopwatch.paused:
				for thehero in objs.heros:

					if thehero.blockerPress and thehero.numOfBlockers >0:
						thehero.placeBlocker()


					#move hero
					if not thehero.shootPress and not thehero.missilePress:
						if thehero.leftPress:
							thehero.vx -= heroAccel
						if thehero.rightPress:
							thehero.vx += heroAccel
						if thehero.upPress:
							thehero.vy -= heroAccel
						if thehero.downPress:
							thehero.vy += heroAccel

					thehero.x += thehero.vx
					thehero.y += thehero.vy

					if thehero.x <= 0:
						thehero.x = 1
						thehero.vx = 0
					if thehero.y <= 0:
						thehero.y = 1
						thehero.vy = 0
					if thehero.x >= screenSize[0]:
						thehero.x = screenSize[0]-1
						thehero.vx = 0
					if thehero.y >= screenSize[1]:
						thehero.y = screenSize[1]-1
						thehero.vy = 0

				#move missiles
				for missile in objs.missiles:
					missile.move()

					for zombie in objs.zombies:
						if abs(missile.x - zombie.x) <= heroRadius and abs(missile.y - zombie.y) <= heroRadius and missile.isAlive:
							missile.isAlive = False
							if not zombie.strong:
								zombie.isAlive = False

				#pick up care packages
				for package in objs.packages:
					for thehero in objs.heros:
						if abs(package.x - thehero.x) <= heroRadius + 5 and abs(package.y - thehero.y) <= heroRadius + 5:
							thehero.numOfMissiles += missilesInPackage
							thehero.numOfBlockers += blockersInPackage
							if zombieCount/zombiesBetweenPackage >= 4:
								thehero.numOfMissiles += 2
								thehero.numOfBlockers += 2
							package.isAlive = False

				#move bullets
				for bullet in objs.bullets:
					bullet.move()
					for thehero in objs.heros:
						if abs(bullet.x - thehero.x) <= heroRadius and abs(bullet.y - thehero.y) <= heroRadius:
							thehero.isAlive = False
							bullet.isAlive = False

					for blocker in objs.blockers:
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


				if stopwatch.getTime() > timeBetweenPackages * packageCount - timeBetweenZombies:
					if not readyForLevel:
						stopwatch.wait(10)
						readyForLevel = True
					else:
						objs.packages.append(CarePackage(ii.next(), screen, randint(0,screenSize[0]),randint(0,screenSize[1])))
						packageCount += 1
						readyForLevel = False


				#move zombies
				if stopwatch.getTime() > timeBetweenZombies * zombieCount:
					randomizer = randint(0,zombieCount/zombiesBetweenPackage)*randint(0,zombieCount/zombiesBetweenPackage) * 2 * zombiesBetweenPackage/(zombieCount+1)
					smart = (randint(0,zombieCount/zombiesBetweenPackage + 3) >= 6)
					strong = (randint(1,zombiesBetweenPackage)==1)
					objs.zombies.append(Zombie(ii.next(),screen, objs.heros, zombieSpeed+randomizer,smart,strong))
					zombieCount+=1

				for zombie in objs.zombies:
					zombie.move()
					for thehero in objs.heros:
						if abs(zombie.x - thehero.x) <= 2*heroRadius and abs(zombie.y - thehero.y) <= 2*heroRadius:
							thehero.isAlive = False

					for bullet in objs.bullets:
						if abs(bullet.x - zombie.x) <= heroRadius and abs(bullet.y - zombie.y) <= heroRadius and bullet.isAlive:
							bullet.isAlive = False
							zombie.isAlive = False


					for blocker in objs.blockers:
						while blocker.contains(zombie):
							blocker.smash()
							zombie.x -= zombie.vx
							zombie.y -= zombie.vy

			sendAdditionalInfo += 1
			#DRAW AND SEND INFO
			screen.fill(BLACK)

			for blocker in objs.blockers:
				for thehero in objs.heros:
					if thehero.client != SENTINEL:
						thehero.client.send("_" + str(BLOCKER) + str(blocker.id).zfill(5) + str(int(blocker.x)).zfill(4) + str(int(blocker.y)).zfill(4) + str(blocker.health).zfill(4) + str(int(blocker.isAlive)))
				blocker.draw()

			for package in objs.packages:
				for thehero in objs.heros:
					if thehero.client != SENTINEL:
						thehero.client.send("_" + str(PACKAGE) + str(package.id).zfill(5) + str(package.x).zfill(4) + str(package.y).zfill(4) + str(int(package.isAlive)))
				package.draw()

			for thehero in objs.heros:
				for ahero in objs.heros:
					if ahero.client != SENTINEL:
						ahero.client.send("_" + str(HERO) + str(thehero.id).zfill(5) + str(int(thehero.x)).zfill(4) + str(int(thehero.y)).zfill(4) + str(thehero.direction) + str(int(thehero.isAlive)))
				thehero.draw()

				if thehero.client != SENTINEL and sendAdditionalInfo > 20:
					thehero.client.send("_INFO: " + str(thehero.numOfMissiles).zfill(3) + str(thehero.numOfBlockers).zfill(3) + str(zombieCount/zombiesBetweenPackage + 1).zfill(2))
					sendAdditionalInfo = 0

			for zombie in objs.zombies:
				for thehero in objs.heros:
					if thehero.client != SENTINEL:
						thehero.client.send("_" + str(ZOMBIE) + str(zombie.id).zfill(5) + str(int(zombie.x)).zfill(4) + str(int(zombie.y)).zfill(4) + str(zombie.direction) + str(int(zombie.strong)) + str(zombie.smartness).zfill(4) + str(int(zombie.isAlive)))
				zombie.draw()

			for missile in objs.missiles:
				for thehero in objs.heros:
					if thehero.client != SENTINEL:
						thehero.client.send("_" + str(MISSILE) + str(missile.id).zfill(5) + str(int(missile.x)).zfill(4) + str(int(missile.y)).zfill(4) + str(missile.direction) + str(int(missile.isAlive)))
				missile.draw()

			for bullet in objs.bullets:
				for thehero in objs.heros:
					if thehero.client != SENTINEL:
						thehero.client.send("_" + str(BULLET) + str(bullet.id).zfill(5) + str(int(bullet.x)).zfill(4) + str(int(bullet.y)).zfill(4) + str(bullet.health).zfill(2) + str(int(bullet.isAlive)))
				bullet.draw()


			#DELETE STUFF

			for i, bullet in enumerate(objs.bullets):
				if not bullet.isAlive:
					del objs.bullets[i]

			for i, zombie in enumerate(objs.zombies):
				if not zombie.isAlive:
					del objs.zombies[i]

			for i, blocker in enumerate(objs.blockers):
				if not blocker.isAlive:
					del objs.blockers[i]

			for i, missile in enumerate(objs.missiles):
				if not missile.isAlive:
					del objs.missiles[i]

			for i, package in enumerate(objs.packages):
				if not package.isAlive:
					del objs.packages[i]

			for i, thehero in enumerate(objs.heros):
				if not thehero.isAlive:
					if thehero.client != SENTINEL:
						thehero.client.send("_INDEX: " + str(SENTINEL))
					del objs.heros[i]
					j = 0
					for thehero in objs.heros:
						if j != 0 or not hero.isAlive:
							thehero.client.send("_INDEX: " + str(j))
						j += 1

			if len(objs.heros) == 0:
				gameOver = True



			hud = hudFont.render("MISSILES: " + str(hero.numOfMissiles) + "  BLOCKERS: " + str(hero.numOfBlockers), False, WHITE)
			screen.blit(hud,(5,screenSize[1]-17))

			if (readyForLevel and int(stopwatch.getTime()/500)%2) or not readyForLevel:
				title = titleFont.render("LEVEL " + str(zombieCount/zombiesBetweenPackage + 1), False, WHITE)
				screen.blit(title,(screenSize[0]-120, 5))

			if gameOver:
				title = titleFont.render("GAME OVER", False, WHITE)
				screen.blit(title,(screenSize[0]/2-50, screenSize[1]/2-20))

			if stopwatch.paused:
				title = titleFont.render("PAUSED", False, WHITE)
				screen.blit(title,(screenSize[0]/2-50, screenSize[1]/2-20))

			#UPDATE
			pygame.display.flip()
			clock.tick(20) #Limit frames per second

		if gameOver:
			pygame.time.wait(2500)

			playAgain = False
			screen.fill(BLACK)
			title = titleFont.render("YOU MADE IT TO LEVEL " + str(zombieCount/zombiesBetweenPackage + 1), False, WHITE)
			screen.blit(title,(screenSize[0]/2-140, screenSize[1]/2-60))
			title = titleFont.render("PRESS ANY KEY TO PLAY AGAIN", False, WHITE)
			screen.blit(title,(screenSize[0]/2-170, screenSize[1]/2-20))
			pygame.display.flip()

			#bleed event list
			for event in pygame.event.get():
				pass
			del objs.bullets[:]
			del objs.blockers[:]
			del objs.zombies[:]
			del objs.missiles[:]
			del objs.packages[:]
			del objs.heros[:]

			while not playAgain:
				for event in pygame.event.get():

					if event.type == pygame.QUIT:
						quit = True

					elif event.type == pygame.KEYDOWN:
						playAgain = True
						readyForLevel = True

				if quit:
					break

				time.sleep(0.1)

	pygame.quit()



if __name__ == '__main__': #for testing, run 'python serverGame.py' instead of initUI.py
	start([])
