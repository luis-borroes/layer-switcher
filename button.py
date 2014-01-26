import pygame

class Button(object):
	group = []
	imgBig = pygame.image.load("assets/sprites/menuBig.png")
	imgMedium = pygame.image.load("assets/sprites/menuMedium.png")
	imgSmall = pygame.image.load("assets/sprites/menuSmall.png")

	def __init__(self, bType, font, text, pos, resolution, callback):
		self.font = font
		self.setText(text)

		if bType == "text":
			img = None
		elif bType == "big":
			img = Button.imgBig
		elif bType == "medium":
			img = Button.imgMedium
		elif bType == "small":
			img = Button.imgSmall

		if img:
			self.position = pygame.rect.Rect((resolution[0] * 0.5 - img.get_width() * 0.5 + pos[0], pos[1]), img.get_size())
			self.callback = callback

			self.img = img
			self.overlay = pygame.Surface(img.get_size(), pygame.SRCALPHA | pygame.HWSURFACE)
			self.overlay.fill((255, 255, 255, 60))
			self.overlay.convert_alpha()

		else:
			self.img = None
			self.position = pygame.rect.Rect((resolution[0] * 0.5 - self.textSize[0] * 0.5 + pos[0], pos[1]), self.textSize)
			self.callback = None

		Button.group.append(self)

	def updateAndDraw(self, screen, mPos, trigger):
		if self.img:
			screen.blit(self.img, self.position.topleft)

		screen.blit(self.text, (self.position.centerx - self.textSize[0] * 0.5, self.position.centery - self.textSize[1] * 0.5))

		if mPos[0] in xrange(self.position.left, self.position.right) and mPos[1] in xrange(self.position.top, self.position.bottom) and self.img and self.callback:
			screen.blit(self.overlay, self.position.topleft)

			if trigger:
				self.callback()

	def setText(self, text):
		self.text = self.font.render(str(text), 1, (0, 0, 0))
		self.textSize = self.font.size(str(text))
