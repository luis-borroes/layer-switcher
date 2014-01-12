import pygame, game, sys, utils, animation
util = utils.Utils()

class Menu(object):

	def __init__(self, screen, clock, fps, resolution, version):
		self.running = True

		self.img = pygame.image.load("assets/sprites/menu.png").convert_alpha()
		self.logo = animation.Animation("assets/characters/player/standingRight.png", 50, 50, 2, 2)
		self.splice = self.logo.getSplice()
		self.background = pygame.image.load("assets/sprites/backgrounds/world1.png").convert_alpha()
		self.bgPos = (0, 0)

		self.mediumFont = pygame.font.Font("assets/ARLRDBD.ttf", 30)
		self.bigFont = pygame.font.Font("assets/ARLRDBD.ttf", 72)

		self.mainText = self.bigFont.render("Layer Switcher", 1, (0, 0, 0))
		self.versionText = self.mediumFont.render(version, 1, (0, 0, 0))

		self.args = [screen, clock, fps, self.mediumFont, resolution]

		Option(self.img, self.mediumFont, "Start", (resolution[0] // 2 - self.img.get_width() // 2, resolution[1] - 300), self.start)
		Option(self.img, self.mediumFont, "Quit", (resolution[0] // 2 - self.img.get_width() // 2, resolution[1] - 225), self.leave)

		while self.running:
			dt = clock.tick(fps)

			mouseTrigger = False

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.leave()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.leave()

					if event.key == pygame.K_SPACE:
						self.start()

				if event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						mouseTrigger = True

			screen.fill((82, 246, 255))

			mPos = pygame.mouse.get_pos()

			self.bgPos = (
				-util.remap(mPos[0], 0, resolution[0], 0, self.background.get_width() - resolution[0]),
				-util.remap(mPos[1], 0, resolution[1], 0, self.background.get_height() - resolution[1])
			)

			screen.blit(self.background, self.bgPos)
			screen.blit(self.mainText, (resolution[0] // 2 - self.mainText.get_width() // 2, 100))
			screen.blit(self.versionText, (5, resolution[1] - self.versionText.get_height() - 5))

			self.logo.update(dt * 0.001)
			screen.blit(self.splice, (resolution[0] // 2 - self.splice.get_width() // 2, 270))

			for opt in Option.group:
				opt.updateAndDraw(screen, mPos, mouseTrigger)

			pygame.display.flip()

	def start(self):
		self.game = game.Game(*self.args)
		pygame.display.set_caption("Layer Switcher", "Layer Switcher")

	def leave(self):
		self.running = False
		pygame.quit()
		sys.exit(0)

class Option(object):
	group = []

	def __init__(self, img, font, text, pos, callback):
		self.img = img
		self.overlay = pygame.Surface(img.get_size(), pygame.SRCALPHA)
		self.overlay.fill((255, 255, 255, 60))
		self.overlay.convert_alpha()

		self.text = font.render(text, 1, (0, 0, 0))
		self.textSize = font.size(text)

		self.position = pygame.rect.Rect(pos, img.get_size())
		self.callback = callback

		Option.group.append(self)

	def updateAndDraw(self, screen, mPos, trigger):
		screen.blit(self.img, self.position.topleft)
		screen.blit(self.text, (self.position.centerx - self.textSize[0] // 2, self.position.centery - self.textSize[1] // 2))

		if mPos[0] in xrange(self.position.left, self.position.right) and mPos[1] in xrange(self.position.top, self.position.bottom):
			screen.blit(self.overlay, self.position.topleft)

			if trigger:
				self.callback()
