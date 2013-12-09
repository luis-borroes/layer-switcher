import pygame

from vector import Vec2d as Vector

class Player(pygame.sprite.Sprite):

	def __init__(self, objMap, *groups):
		super(Player, self).__init__(*groups)

		self.map = objMap.map

		self.image = pygame.image.load('assets/player.png')
		self.rect = pygame.rect.Rect((360, 300), self.image.get_size())

		self.position = pygame.rect.Rect((0, 0), self.image.get_size())
		self.acceleration = Vector(0, 0)
		self.resting = False
		self.jumping = False
		self.layer = 0
		self.lastLayer = self.layer

		objects = self.map.getObjects()
		for obj in objects:
			if obj.name == "spawn":
				self.position.x = obj.x - 25 + self.map.tilewidth / 2
				self.position.y = obj.y - 15 - self.map.tileheight

	def update(self, dt, game):
		last = self.position.copy()
		
		keys = pygame.key.get_pressed()

		if keys[pygame.K_a]:
			self.acceleration.x = self._approach_(dt, self.acceleration.x, -400, 20)
		if keys[pygame.K_d]:
			self.acceleration.x = self._approach_(dt, self.acceleration.x, 400, 20)

		if keys[pygame.K_SPACE]:
			if self.resting:
				self.jumping = True
				self.acceleration.y = -800
			elif self.jumping:
				self.acceleration.y = self._approach_(dt, self.acceleration.y, -350, 1)
				if self.acceleration.y == -350:
					self.jumping = False
		else:
			self.jumping = False

		if not self.resting:
			self.acceleration.y = self._approach_(dt, self.acceleration.y, 400, 20)
		else:
			self.acceleration.x = self._approach_(dt, self.acceleration.x, 0, 50)

		self.position.x += self.acceleration.x * dt
		self.position.y += self.acceleration.y * dt

		self.resting = False

		for block in game.map.layers[self.layer]:
			if self.position.colliderect(block.position):
				cell = block.position

				if "l" in block.prop and self.position.right > cell.left and last.right <= cell.left:
					self.position.right = cell.left
					self.acceleration.x = 0

				if "r" in block.prop and self.position.left < cell.right and last.left >= cell.right:
					self.position.left = cell.right
					self.acceleration.x = 0

				if "u" in block.prop and self.position.bottom > cell.top and last.bottom <= cell.top:
					self.position.bottom = cell.top
					self.resting = True
					self.acceleration.y = 0

				if "d" in block.prop and self.position.top < cell.bottom and last.top >= cell.bottom:
					self.position.top = cell.bottom
					self.acceleration.y = 0

		self.lastLayer = self.layer

	def _approach_(self, dt, num, target, step):
		if num > target:
			return max(num - step * dt * 100, target)
		elif num < target:
			return min(num + step * dt * 100, target)
		return num