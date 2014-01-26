import pygame, sys, os, utils, animation, button, options, world
util = utils.Utils()

class Menu(object):

	def __init__(self, screen, clock, fps, resolution, version):
		self.screen = screen
		self.clock = clock
		self.fps = fps
		self.resolution = resolution
		self.halfResolution = (self.resolution[0] // 2, self.resolution[1] // 2)
		self.version = version
		self.volume = pygame.mixer.music.get_volume()

		self.running = True

		for anim in os.listdir("assets/characters/player"):
			info = anim[:anim.find(".")].split("+")
			if info[0] == "standingRight":
				self.logo = animation.Animation("assets/characters/player/%s" % anim, 50, 50, float(info[1]), float(info[2]))
				self.splice = self.logo.getSplice()

		self.background = pygame.image.load("assets/sprites/backgrounds/world1.png").convert_alpha()
		self.bgPos = (0, 0)

		self.mediumFont = pygame.font.Font("assets/ARLRDBD.ttf", 30)
		self.bigFont = pygame.font.Font("assets/ARLRDBD.ttf", 72)

		self.mainText = self.bigFont.render("Layer Switcher", 1, (0, 0, 0))
		self.versionText = self.mediumFont.render(self.version, 1, (0, 0, 0))

		self.currentMenu = ""

		self.mainMenu()

		while self.running:
			dt = self.clock.tick(self.fps)
			pygame.display.set_caption("Layer Switcher %3d FPS" % (self.clock.get_fps()), "Layer Switcher")

			mouseTrigger = False

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.leave()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						if self.currentMenu == "main":
							self.leave()
						else:
							self.mainMenu()

					if event.key == pygame.K_SPACE:
						if self.currentMenu == "main":
							world.World(self)
						elif self.currentMenu == "world":
							self.world.start()

				if event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						mouseTrigger = True

			self.screen.fill((82, 246, 255))

			mPos = pygame.mouse.get_pos()

			self.bgPos = (
				-util.remap(mPos[0], 0, self.resolution[0], 0, self.background.get_width() - self.resolution[0]),
				-util.remap(mPos[1], 0, self.resolution[1], 0, self.background.get_height() - self.resolution[1])
			)

			self.screen.blit(self.background, self.bgPos)
			self.screen.blit(self.mainText, (self.halfResolution[0] - self.mainText.get_width() // 2, 100))
			self.screen.blit(self.versionText, (5, self.resolution[1] - self.versionText.get_height()))

			if self.currentMenu == "main":
				self.logo.update(dt * 0.001)
				self.screen.blit(self.splice, (self.halfResolution[0] - self.splice.get_width() // 2, 270))

			for opt in button.Button.group:
				opt.updateAndDraw(self.screen, mPos, mouseTrigger)

			pygame.display.flip()

	def mainMenu(self):
		self.currentMenu = "main"

		button.Button.group = []

		button.Button("big", self.mediumFont, "World", (0, self.resolution[1] - 300), self.resolution, lambda: world.World(self))
		button.Button("big", self.mediumFont, "Options", (0, self.resolution[1] - 225), self.resolution, lambda: options.Options(self))
		button.Button("big", self.mediumFont, "Quit", (0, self.resolution[1] - 150), self.resolution, self.leave)

	def leave(self):
		self.running = False
		pygame.quit()
		sys.exit(0)
