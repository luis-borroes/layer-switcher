import pygame

class Animation(object):
	loadedImagePaths = []
	loadedImages = []

	def __init__(self, imgPath, width, height, updateRate, frameLimit):
		if imgPath not in Animation.loadedImagePaths:
			self.img = pygame.image.load(imgPath).convert_alpha()
			Animation.loadedImagePaths.append(imgPath)
			Animation.loadedImages.append(self.img)
		else:
			self.img = Animation.loadedImages[Animation.loadedImagePaths.index(imgPath)]

		self.width = width
		self.height = height
		self.frameList = self.genLoopable(self.img.get_width(), self.img.get_height())
		self.position = pygame.rect.Rect((0, 0), (self.width, self.height))
		self.surface = pygame.Surface(self.position.size, pygame.SRCALPHA).convert_alpha()
		self.rate = 1 / float(updateRate)
		self.swapTimer = 0
		self.frame = 0
		self.frameLimit = frameLimit
		self.callback = None

		self.setPos(self.position.topleft)

	def genLoopable(self, width, height):
		posList = []

		for y in xrange(height / self.height):
			for x in xrange(width / self.width):
				posList.append((x, y))

		return posList

	def setPos(self, pos):
		self.position.topleft = (pos[0] * self.width, pos[1] * self.height)
		self.surface.fill(0)
		self.surface.blit(self.img, (-self.position.x, -self.position.y))

	def getSplice(self):
		return self.surface

	def setCallback(self, callback):
		self.callback = callback

	def update(self, dt):
		self.swapTimer = min(self.rate, self.swapTimer + dt)

		if self.swapTimer == self.rate:
			self.swapTimer = 0
			self.frame += 1

			if self.frame == self.frameLimit:
				self.frame = 0

				if self.callback:
					self.callback()

			self.setPos(self.frameList[self.frame])
