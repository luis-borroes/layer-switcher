import pygame, vector

class Button(object):
	group = []
	imgBig = pygame.image.load("assets/sprites/menuBig.png")
	imgMedium = pygame.image.load("assets/sprites/menuMedium.png")
	imgSmall = pygame.image.load("assets/sprites/menuSmall.png")

	def __init__(self, bType, font, text, pos, resolution, callback):
		self.font = font
		self.setText(text)

		self.locked = False

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

			self.lockedOverlay = pygame.Surface(img.get_size(), pygame.SRCALPHA | pygame.HWSURFACE)
			self.lockedOverlay.fill((0, 0, 0, 100))
			self.lockedOverlay.convert_alpha()

		else:
			self.img = None
			self.position = pygame.rect.Rect((resolution[0] * 0.5 - self.textSize[0] * 0.5 + pos[0], pos[1]), self.textSize)
			self.callback = None

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
		self.text = self.font.render(str(text), 1, (0, 0, 0))
		self.textSize = self.font.size(str(text))

class MovingText(object):

	def __init__(self, text, font, pos, final):
		self.font = font
		self.pos = vector.Vec2d(pos)
		self.final = vector.Vec2d(final)
		self.vector = self.final - self.pos

		self.setText(text)

	def setText(self, text):
		self.text = text
		self.rendered = self.font.render(self.text, 1, (0, 0, 0))
		self.pos -= (self.rendered.get_width() * 0.5, self.rendered.get_height() * 0.5)
		self.final -= (self.rendered.get_width() * 0.5, self.rendered.get_height() * 0.5)

	def updateAndDraw(self, parent):
		if self.vector.length > 0:
			vec = self.vector * 0.005 * parent.dt
			if vec.length < 0.05:
				self.pos = self.final
				self.vector = vector.Vec2d(0, 0)

			else:
				self.pos += vec
				self.vector = self.final - self.pos

		parent.screen.blit(self.rendered, self.pos)
