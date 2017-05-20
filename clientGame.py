from gamePlay import *
import time
import sys #for debugging

lengthsOfMessages = []

def start(server):
	start = False
	hasIndex = False
	while not (start and hasIndex):
		for message in server.get():
			if message == "START":
				start = True
			if message[0:5] == "INDEX":
				index = int(message[-1])
				hasIndex = True
		time.sleep(.01)
		if not server.isAlive:
			return

	print "Loading..."
	sys.stdout.flush()

	pygame.init()
	pygame.display.set_caption("Swarm (Client Game)")
	screen = pygame.display.set_mode(screenSize)

	print "Pygame initiated"
	sys.stdout.flush()

	clock = pygame.time.Clock()
	pygame.mouse.set_visible(0)

	hudFont = pygame.font.SysFont("Courier New", 12)
	titleFont = pygame.font.SysFont("Courier New", 20)

	level = 1
	numOfBlockers = 0
	numOfMissiles = 0

	quit = False
	while server.isAlive and not quit:

		for message in server.get():
			if message[:5] == "INDEX":
				index = int(message[7:])
			elif message[:4] == "INFO":
				numOfMissiles = int(message[6:9])
				numOfBlockers = int(message[9:12])
				level = int(message[12:14])
			else:
				try:
					objs.handle_command(message, screen)
				except:
					print "ERROR: Bad message: " + message

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit = True
			elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
				server.send("_" + str(int(event.type == pygame.KEYDOWN)) + str(event.key))

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
				del objs.heros[i]

		#DRAW
		screen.fill(BLACK)

		for blocker in objs.blockers:
			blocker.draw()

		for package in objs.packages:
			package.draw()

		for thehero in objs.heros:
			thehero.draw()

		for zombie in objs.zombies:
			zombie.draw()

		for missile in objs.missiles:
			missile.draw()

		for bullet in objs.bullets:
			bullet.draw()

		if len(objs.heros) != 0:
			hud = hudFont.render("MISSILES: " + str(numOfMissiles) + "  BLOCKERS: " + str(numOfBlockers), False, WHITE)
			screen.blit(hud,(5,screenSize[1]-17))

			title = titleFont.render("LEVEL " + str(level), False, WHITE)
			screen.blit(title,(screenSize[0]-120, 5))

		if index == SENTINEL:
			for event in pygame.event.get():
				pass
			del objs.bullets[:]
			del objs.blockers[:]
			del objs.zombies[:]
			del objs.missiles[:]
			del objs.packages[:]
			del objs.heros[:]
			quit = False
			while index == SENTINEL:
				for message in server.get():
					if message[:5] == "INDEX":
						index = int(message[7:])
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						quit = True

				screen.fill(BLACK)

				title = titleFont.render("WAITING FOR NEW GAME", False, WHITE)
				screen.blit(title,(screenSize[0]/2-130, screenSize[1]/2-20))

				if not server.isAlive:
					return
				if quit:
					break

				pygame.display.flip()
				clock.tick(10)


		pygame.display.flip()
		clock.tick(20)

	pygame.quit()
