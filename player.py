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
		self.cdBar = pygame.rect.Rect((self.rect.left, self.rect.bottom + 2), (0, 10))

	def spawn(self):
		self.rect = pygame.rect.Rect((0, 0), self.image.get_size())

		self.position = pygame.rect.Rect((0, 0), self.image.get_size())
		self.acceleration = Vector(0, 0)
		self.resting = False
		self.jumping = False
		self.jumpTimer = 0
		self.spaced = False
		self.key_w = False
		self.key_s = False
		self.layer = 0
		self.layerChanging = False
		self.layerCooldown = 0
		self.oldAccel = 0

		for obj in self.map.getObjects():
			if obj.name == "spawn":
				self.position.x = obj.x + (self.map.tilewidth / 2 - self.rect.width / 2)
				self.position.y = obj.y - (self.rect.height - self.map.tileheight)
				if hasattr(obj, "layer"):
					self.layer = int(obj.layer)

		self.layerOffset = 70 * self.layer

	def update(self, game, dt):
		last = self.position.copy()

		self.layerCooldown = max(0, self.layerCooldown - dt)

		if self.key_w:
			self.key_w = False
			if self.layerCooldown == 0 and self.layer > 0:
				walled = False
				destination = self.position.copy()
				destination.y -= 71
				for block in game.map.layers[self.layer - 1]:
					if block.collidable and util.collide(destination, block.position):
						walled = True

				if not walled:
					self.layer -= 1
					self.layerChanging = True
					self.acceleration.y = 0
					self.layerCooldown = 0.5

		if self.key_s:
			self.key_s = False
			if self.layerCooldown == 0 and self.layer < len(game.map.layers) - 1:
				walled = False
				destination = self.position.copy()
				destination.y += 69
				for block in game.map.layers[self.layer + 1]:
					if block.collidable and util.collide(destination, block.position):
						walled = True

				if not walled:
					self.layer += 1
					self.layerChanging = True
					self.acceleration.y = 0
					self.layerCooldown = 0.5

		self.cdBar = pygame.rect.Rect((self.rect.left, self.rect.bottom + 2), (util.remap(self.layerCooldown, 0, 0.5, 0, self.rect.width), 5))
		
		keys = pygame.key.get_pressed()

		if keys[pygame.K_a]:
			self.acceleration.x = util.approach(dt, self.acceleration.x, -400, 20)
		if keys[pygame.K_d]:
			self.acceleration.x = util.approach(dt, self.acceleration.x, 400, 20)

		if self.spaced:
			self.spaced = False

			if not self.layerChanging and not self.jumping and self.resting:
				self.jumping = True
				self.acceleration.y = -600
				self.resting = False
				self.spaced = False

		if keys[pygame.K_SPACE] and self.jumping:
			self.jumpTimer += 1
			self.acceleration.y = util.approach(dt, self.acceleration.y, -600, 20)
			if self.jumpTimer == 35:
				self.jumping = False
				self.jumpTimer = 0
		elif self.jumping:
			self.jumping = False

		if not self.resting:
			self.acceleration.y = util.approach(dt, self.acceleration.y, 500, 20)
		elif not self.layerChanging:
			self.acceleration.x = util.approach(dt, self.acceleration.x, 0, 10)

		self.position.x += int(round(self.acceleration.x * dt))
		self.position.y += int(round(self.acceleration.y * dt))

		if self.position.x < 0:
			self.position.x = 0
			self.acceleration.x = 0

		if self.position.right > game.map.width:
			self.position.right = game.map.width

		if self.position.y > game.map.height + 200:
			self.spawn()

		self.resting = False

		if self.layerChanging:
			self.resting = True
			oldOff = self.layerOffset
			self.layerOffset = util.approach(dt, self.layerOffset, 70 * self.layer, 5)

			if self.layerOffset == oldOff:
				self.layerChanging = False
				self.resting = False
				self.acceleration.y = self.oldAccel

			self.position.y += self.layerOffset - self.oldOff
		else:
			self.oldAccel = self.acceleration.y

		self.oldOff = self.layerOffset

		for block in game.map.layers[self.layer]:
			if block.collidable and util.collide(self.position, block.position):
				cell = block.position

				siding = False

				if "l" in block.prop and self.position.right >= cell.left and last.right <= cell.left:
					self.position.right = cell.left
					siding = True
					if self.acceleration.x > 0:
						self.acceleration.x = 0

				if "r" in block.prop and self.position.left <= cell.right and last.left >= cell.right:
					self.position.left = cell.right
					siding = True
					if self.acceleration.x < 0:
						self.acceleration.x = 0

				if "u" in block.prop and self.position.bottom >= cell.top and last.bottom <= cell.top and not siding:
					self.position.bottom = cell.top
					self.resting = True
					if self.acceleration.y > 0:
						self.acceleration.y = 0

				if "d" in block.prop and self.position.top <= cell.bottom and last.top >= cell.bottom and not siding:
					self.position.top = cell.bottom
					if self.acceleration.y < 0:
						self.acceleration.y = 0

	def draw(self, screen):
		self.sprites.draw(screen)

		if self.cdBar.width > 0:
			pygame.draw.rect(screen, (190, 0, 0), self.cdBar)
