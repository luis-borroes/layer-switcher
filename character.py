import pygame

from vector import Vec2d as Vector
from utils import Utils
util = Utils()

class Character(pygame.sprite.Sprite):

	def __init__(self, objMap, charType, pos, layer):
		self.sprites = pygame.sprite.Group()
		super(Character, self).__init__(self.sprites)

		self.map = objMap
		self.type = charType
		self.setStatus("standing")

		self.startPos = pos
		self.startLayer = layer
		self.moveSpeed = 500
		self.gravity = 600
		self.jumpSpeed = -600
		self.jumpTimerLimit = 35
		self.swimSpeed = -400

		if hasattr(self.map.tilemap, "gravity"):
			self.gravity = int(self.map.tilemap.gravity)

		self.spawn()

	def spawn(self):
		self.rect = pygame.rect.Rect((0, 0), self.image.get_size())
		self.position = pygame.rect.Rect(self.startPos, self.image.get_size())
		self.acceleration = Vector(0, 0)
		self.speedModifier = 1
		self.resting = False
		self.jumping = False
		self.jumpTimer = 0
		self.holdJump = False
		self.layer = self.startLayer
		self.drawLayer = self.startLayer
		self.layerChanging = False
		self.layerCooldown = 0
		self.layerOffset = 70 * self.layer
		self.oldAccel = 0
		self.swimming = False

	def die(self):
		pass

	def jump(self):
		if not self.layerChanging and not self.jumping and not self.swimming and self.resting:
			self.jumping = True
			self.acceleration.y = self.jumpSpeed
			self.resting = False

	def moveLeft(self, dt):
		self.acceleration.x = util.approach(dt, self.acceleration.x, -self.moveSpeed, 20)

	def moveRight(self, dt):
		self.acceleration.x = util.approach(dt, self.acceleration.x, self.moveSpeed, 20)

	def toBack(self, game):
		if self.layerCooldown == 0 and self.layer > 0:
			walled = False
			destination = self.position.copy()
			destination.y -= 71
			for block in self.getNearbyBlocks(self.layer - 1, 2):
				if block.collidable and util.collide(destination, block.position):
					walled = True

			if not walled:
				self.layer -= 1
				self.layerChanging = True
				self.acceleration.y = 0
				self.layerCooldown = 0.5

	def toFront(self, game):
		if self.layerCooldown == 0 and self.layer < len(game.map.layers) - 1:
			walled = False
			destination = self.position.copy()
			destination.y += 69
			for block in self.getNearbyBlocks(self.layer + 1, 2):
				if block.collidable and util.collide(destination, block.position):
					walled = True

			if not walled:
				self.layer += 1
				self.drawLayer = self.layer
				self.layerChanging = True
				self.acceleration.y = 0
				self.layerCooldown = 0.5

	def update(self, game, dt):
		last = self.position.copy()

		self.layerCooldown = max(0, self.layerCooldown - dt)

		if self.holdJump:
			if self.jumping:
				self.jumpTimer += 1
				self.acceleration.y = util.approach(dt, self.acceleration.y, self.jumpSpeed, 20)
				if self.jumpTimer == self.jumpTimerLimit:
					self.jumping = False
					self.jumpTimer = 0
			elif self.swimming:
				self.acceleration.y = util.approach(dt, self.acceleration.y, self.swimSpeed, 50)
		elif self.jumping:
			self.jumping = False

		if self.resting:
			self.acceleration.x = util.approach(dt, self.acceleration.x, 0, 10)
		elif not self.layerChanging:
			self.acceleration.y = util.approach(dt, self.acceleration.y, self.gravity, 20)

		if self.swimming:
			self.acceleration.x = util.approach(dt, self.acceleration.x, 0, 10)

		self.position.x += int(round(self.acceleration.x * dt * self.speedModifier))
		self.position.y += int(round(self.acceleration.y * dt * self.speedModifier))

		self.speedModifier = 1

		if self.position.x < 0:
			self.position.x = 0
			self.acceleration.x = 0

		if self.position.right > game.map.width:
			self.position.right = game.map.width
			self.acceleration.x = 0

		if self.position.y > game.map.height + 250:
			self.spawn()

		self.resting = False
		self.swimming = False

		if self.layerChanging:
			self.resting = True
			oldOff = self.layerOffset
			self.layerOffset = util.approach(dt, self.layerOffset, 70 * self.layer, 5)

			if self.layerOffset == oldOff:
				self.layerChanging = False
				self.resting = False
				self.acceleration.y = self.oldAccel
				self.drawLayer = self.layer

			self.position.y += self.layerOffset - self.oldOff
		else:
			self.oldAccel = self.acceleration.y

		self.oldOff = self.layerOffset

		for block in self.getNearbyBlocks(self.layer, 2):
			if util.collide(self.position, block.position):
				cell = block.position

				if block.collidable:
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

				if "s" in block.prop:
					self.speedModifier = 0.2

				if "w" in block.prop:
					self.swimming = True
					self.speedModifier = 0.5

				if "k" in block.prop:
					self.die()

	def draw(self, screen):
		self.sprites.draw(screen)

	def setStatus(self, status):
		self.image = pygame.image.load('assets/characters/%s/%s.png' % (self.type, status))

	def getNearbyBlocks(self, layer, tileRadius):
		d = []

		for i in xrange(tileRadius * 2):
			for j in xrange(tileRadius * 2):
				if (layer, self.position.centerx / self.map.tilemap.tilewidth + i - tileRadius, self.position.centery / self.map.tilemap.tileheight + j - tileRadius) in self.map.blocks:
					d.append(self.map.blocks[(layer, self.position.centerx / self.map.tilemap.tilewidth + i - tileRadius, self.position.centery / self.map.tilemap.tileheight + j - tileRadius)])

		return d
