import pygame

from vector import Vec2d as Vector
from utils import Utils
util = Utils()

class Player(pygame.sprite.Sprite):

	def __init__(self, objMap):
		self.sprites = pygame.sprite.Group()
		super(Player, self).__init__(self.sprites)

		self.map = objMap.map
		self.image = pygame.image.load('assets/player.png')
		self.spawn()

	def spawn(self):
		self.rect = pygame.rect.Rect((0, 0), self.image.get_size())

		self.position = pygame.rect.Rect((0, 0), self.image.get_size())
		self.acceleration = Vector(0, 0)
		self.resting = False
		self.jumping = False
		self.layer = 0
		self.layerChanging = False
		self.oldAccel = 0

		objects = self.map.getObjects()
		for obj in objects:
			if obj.name == "spawn":
				self.position.x = obj.x + (self.map.tilewidth / 2 - self.rect.width / 2)
				self.position.y = obj.y - (self.rect.height - self.map.tileheight)
				if hasattr(obj, "layer"):
					self.layer = int(obj.layer)

		self.layerOffset = 70 * self.layer

	def update(self, dt, game):
		last = self.position.copy()
		
		keys = pygame.key.get_pressed()

		if keys[pygame.K_a]:
			self.acceleration.x = util.approach(dt, self.acceleration.x, -400, 20)
		if keys[pygame.K_d]:
			self.acceleration.x = util.approach(dt, self.acceleration.x, 400, 20)

		if keys[pygame.K_SPACE] and not self.layerChanging:
			if self.resting:
				self.jumping = True
				self.acceleration.y = -800
			elif self.jumping:
				self.acceleration.y = util.approach(dt, self.acceleration.y, -350, 1)
				if self.acceleration.y == -350:
					self.jumping = False
		else:
			self.jumping = False

		if not self.resting:
			self.acceleration.y = util.approach(dt, self.acceleration.y, 400, 20)
		else:
			self.acceleration.x = util.approach(dt, self.acceleration.x, 0, 50)

		self.position.x += self.acceleration.x * dt
		self.position.y += self.acceleration.y * dt

		if self.position.x < 0:
			self.position.x = 0
			self.acceleration.x = 0
		if self.position.y > game.map.height + 200:
			self.spawn()

		self.resting = False

		if self.layerChanging:
			self.resting = True
			self.position.y += self.layerOffset - self.oldOff
		else:
			self.oldAccel = self.acceleration.y

		self.oldOff = self.layerOffset

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
