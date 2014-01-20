import pygame, random

class Particles(object):
	groups = []

	def __init__(self, rate, lifeTime, color, position, size):
		self.img = pygame.Surface((5, 5), pygame.SRCALPHA | pygame.HWSURFACE)
		self.img.fill(color)
		self.img.convert_alpha()

		self.rate = 1 / float(rate)
		self.emitDelay = 0
		self.lifeTime = lifeTime
		self.position = pygame.rect.Rect(position, size)
		self.rect = pygame.rect.Rect(position, size)
		self.list = []

		Particles.groups.append(self)

	def add(self, layer):
		self.list.append(Particle(self, layer))

	def emit(self, dt, layer):
		self.emitDelay = min(self.rate, self.emitDelay + dt)

		if self.emitDelay == self.rate:
			self.emitDelay = 0
			self.add(layer)

	def setOffset(self, pos):
		self.rect.topleft = pos

	def update(self, game, position):
		self.position.topleft = position

		for p in self.list:
			if p.update(game.dt * 0.001):
				self.list.remove(p)

	def draw(self, game, layer):
		for p in self.list:
			if p.layer == layer:
				game.screen.blit(self.img, (p.position.x - self.rect.x, p.position.y - self.rect.y))

class Particle(object):

	def __init__(self, group, layer):
		pos_x = random.randint(group.position.left, group.position.right)
		pos_y = random.randint(group.position.top, group.position.bottom)
		self.position = pygame.rect.Rect((pos_x - group.img.get_width() / 2, pos_y - group.img.get_height() / 2), group.img.get_size())
		self.layer = layer

		self.group = group
		self.life = 0

	def update(self, dt):
		self.life = min(self.group.lifeTime, self.life + dt)

		if self.life == self.group.lifeTime:
			return True
