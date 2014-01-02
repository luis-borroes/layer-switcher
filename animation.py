import pygame

class Animation(object):

	def __init__(self, imgPath, width, height, updateRate, frameLimit):
		self.img = pygame.image.load(imgPath).convert_alpha()
		self.width = width
		self.height = height
		self.frameList = self.genLoopable(self.img.get_width(), self.img.get_height())
		self.pos = pygame.rect.Rect((0, 0), (self.width, self.height))
		self.surface = pygame.Surface(self.pos.size, pygame.SRCALPHA)
		self.rate = 1 / float(updateRate)
		self.swapTimer = 0
		self.frame = 0
		self.frameLimit = frameLimit

	def genLoopable(self, width, height):
		posList = []

		for y in xrange(height / self.height):
			for x in xrange(width / self.width):
				posList.append((x, y))

		return posList

	def setPos(self, pos):
		self.pos.topleft = (pos[0] * self.width, pos[1] * self.height)
		self.surface.fill(0)
		self.surface.blit(self.img, (-self.pos.x, -self.pos.y))

	def getSplice(self):
		return self.surface

	def update(self, dt):
		self.swapTimer = min(self.rate, self.swapTimer + dt)

		if self.swapTimer == self.rate:
			self.swapTimer = 0
			self.frame += 1

			if self.frame == self.frameLimit:
				self.frame = 0

		self.setPos(self.frameList[self.frame])
