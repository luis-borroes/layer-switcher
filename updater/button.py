import pygame

class Button(object):
	group = []

	def __init__(self, bType, font, text, pos, resolution, callback = None):
		self.font = font
		self.locked = False

		self.setText(text)

		if bType == "text":
			img = None
		else:
			img = pygame.image.load("assets/sprites/menuBig.png").convert_alpha()

		if img:
			self.position = pygame.rect.Rect((resolution[0] * 0.5 - img.get_width() * 0.5 + pos[0], pos[1]), img.get_size())
			self.callback = callback

			self.overlay = pygame.Surface(img.get_size(), pygame.SRCALPHA | pygame.HWSURFACE)
			self.overlay.fill((255, 255, 255, 60))
			self.overlay.convert_alpha()

			self.lockedOverlay = pygame.Surface(img.get_size(), pygame.SRCALPHA | pygame.HWSURFACE)
			self.lockedOverlay.fill((0, 0, 0, 100))
			self.lockedOverlay.convert_alpha()

		else:
			self.position = pygame.rect.Rect((resolution[0] * 0.5 - self.textSize[0] * 0.5 + pos[0], pos[1]), self.textSize)
			self.callback = None

		self.img = img

		Button.group.append(self)

	def updateAndDraw(self, screen, mPos, trigger):
		if self.img:
			screen.blit(self.img, self.position.topleft)

		screen.blit(self.text, (self.position.centerx - self.textSize[0] * 0.5, self.position.centery - self.textSize[1] * 0.5))

		if self.locked:
			screen.blit(self.lockedOverlay, self.position.topleft)

		elif mPos[0] in xrange(self.position.left, self.position.right) and mPos[1] in xrange(self.position.top, self.position.bottom) and self.img and self.callback:
			screen.blit(self.overlay, self.position.topleft)

			if trigger:
				self.callback()

	def setText(self, text):
		self.rawText = text
		self.text = self.font.render(text, 1, (0, 0, 0))
		self.textSize = self.text.get_size()
