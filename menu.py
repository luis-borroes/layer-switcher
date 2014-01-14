import pygame, game, sys, os, utils, animation
util = utils.Utils()

class Menu(object):

	def __init__(self, screen, clock, fps, resolution, version):
		self.screen = screen
		self.clock = clock
		self.fps = fps
		self.resolution = resolution
		self.halfResolution = (self.resolution[0] // 2, self.resolution[1] // 2)
		self.version = version

		self.running = True

		self.img = pygame.image.load("assets/sprites/menu.png").convert_alpha()
		self.imgSmall = pygame.image.load("assets/sprites/menuSmall.png").convert_alpha()

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
						self.start()

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
			self.screen.blit(self.versionText, (5, self.resolution[1] - self.versionText.get_height() - 5))

			if self.currentMenu == "main":
				self.logo.update(dt * 0.001)
				self.screen.blit(self.splice, (self.halfResolution[0] - self.splice.get_width() // 2, 270))

			for opt in Option.group:
				opt.updateAndDraw(self.screen, mPos, mouseTrigger)

			pygame.display.flip()

	def mainMenu(self):
		self.currentMenu = "main"

		Option.group = []

		Option(self.img, self.mediumFont, "Start", (0, self.resolution[1] - 300), self.resolution, self.start)
		Option(self.img, self.mediumFont, "Options", (0, self.resolution[1] - 225), self.resolution, self.options)
		Option(self.img, self.mediumFont, "Quit", (0, self.resolution[1] - 150), self.resolution, self.leave)

	def options(self):
		self.currentMenu = "options"

		Option.group = []

		Option(None, self.mediumFont, "Set FPS:", (0, self.resolution[1] - 385), self.resolution, None)
		Option(self.imgSmall, self.mediumFont, "30", (-125, self.resolution[1] - 335), self.resolution, lambda: self.setFPS(30.))
		Option(self.imgSmall, self.mediumFont, "60", (0, self.resolution[1] - 335), self.resolution, lambda: self.setFPS(60.))
		Option(self.imgSmall, self.mediumFont, "120", (125, self.resolution[1] - 335), self.resolution, lambda: self.setFPS(120.))

		Option(None, self.mediumFont, "Music volume:", (0, self.resolution[1] - 275), self.resolution, None)
		Option(self.imgSmall, self.mediumFont, "-", (-75, self.resolution[1] - 225), self.resolution, self.lowerVolume)
		Option(self.imgSmall, self.mediumFont, "+", (75, self.resolution[1] - 225), self.resolution, self.raiseVolume)

		Option(self.img, self.mediumFont, "Back", (0, self.resolution[1] - 150), self.resolution, self.mainMenu)

	def setFPS(self, fps):
		self.fps = fps

	def lowerVolume(self):
		new = pygame.mixer.music.get_volume() - 0.05
		pygame.mixer.music.set_volume(new)

	def raiseVolume(self):
		new = pygame.mixer.music.get_volume() + 0.05
		pygame.mixer.music.set_volume(new)

	def start(self):
		self.game = game.Game(self.screen, self.clock, self.fps, self.mediumFont, self.resolution, self.halfResolution)

	def leave(self):
		self.running = False
		pygame.quit()
		sys.exit(0)

class Option(object):
	group = []

	def __init__(self, img, font, text, pos, resolution, callback):
		self.text = font.render(text, 1, (0, 0, 0))
		self.textSize = font.size(text)

		if img:
			self.position = pygame.rect.Rect((resolution[0] // 2 - img.get_width() // 2 + pos[0], pos[1]), img.get_size())
			self.callback = callback

			self.img = img
			self.overlay = pygame.Surface(img.get_size(), pygame.SRCALPHA)
			self.overlay.fill((255, 255, 255, 60))
			self.overlay.convert_alpha()

		else:
			self.img = None
			self.position = pygame.rect.Rect((resolution[0] // 2 - self.textSize[0] // 2 + pos[0], pos[1]), self.textSize)

		Option.group.append(self)

	def updateAndDraw(self, screen, mPos, trigger):
		if self.img:
			screen.blit(self.img, self.position.topleft)

		screen.blit(self.text, (self.position.centerx - self.textSize[0] // 2, self.position.centery - self.textSize[1] // 2))

		if mPos[0] in xrange(self.position.left, self.position.right) and mPos[1] in xrange(self.position.top, self.position.bottom) and self.img:
			screen.blit(self.overlay, self.position.topleft)

			if trigger:
				self.callback()
