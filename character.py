import pygame, utils, animation, particles

from vector import Vec2d as Vector
util = utils.Utils()

class Character(pygame.sprite.Sprite):

	def __init__(self, game, objMap, charType, pos, layer):
		self.sprites = pygame.sprite.Group()
		super(Character, self).__init__(self.sprites)

		self.map = objMap
		self.type = charType

		self.standing = animation.Animation("assets/characters/%s/standingRight.png" % (self.type), 50, 50, 2, 2)

		self.setStatus(self.standing)
		self.shadow = pygame.image.load("assets/sprites/shadow.png")
		self.drawShadow = True

		self.particles = particles.Particles(50, 0.5, (0, 0, 0, 50), (0, 0), (self.image.get_width(), self.map.tilemap.tileheight))
		self.bubbles = particles.Particles(50, 0.5, (0, 0, 255, 50), (0, 0), (self.image.get_width(), self.map.tilemap.tileheight))

		self.startPos = pos
		self.startLayer = layer
		self.moveSpeed = 500
		self.jumpSpeed = -600
		self.jumpTimerLimit = 35
		self.swimSpeed = -400

		if hasattr(self.map.tilemap, "shadow"):
			self.drawShadow = bool(int(self.map.tilemap.shadow))

		self.spawn()

	def spawn(self):
		self.rect = pygame.rect.Rect((0, 0), self.image.get_size())
		self.position = pygame.rect.Rect(self.startPos, self.image.get_size())
		self.velocity = Vector(0, 0)
		self.speedModifier = 1
		self.resting = False
		self.jumping = False
		self.swimming = False
		self.jumpTimer = 0
		self.holdJump = False
		self.layer = self.startLayer
		self.drawLayer = self.startLayer
		self.oldLayer = self.startLayer
		self.layerChanging = False
		self.layerCooldown = 0
		self.layerOffset = 70 * self.layer
		self._oldAccel = 0
		self._oldGround = None
		self._oldResting = False
		self.shadowPos = None
		self.shadowLooking = True

	def die(self):
		pass

	def jump(self):
		if not self.layerChanging and not self.jumping and not self.swimming and self.resting:
			self.jumping = True
			self.velocity.y = self.jumpSpeed
			self.resting = False

	def moveLeft(self, dt):
		self.velocity.x = util.approach(dt, self.velocity.x, -self.moveSpeed, 20)

	def moveRight(self, dt):
		self.velocity.x = util.approach(dt, self.velocity.x, self.moveSpeed, 20)

	def toBack(self, game):
		if self.layerCooldown == 0 and self.layer > 0:
			walled = False
			destination = self.position.copy()
			destination.y -= 71
			for block in self.getNearbyBlocks(self.layer - 1, destination, 1):
				if block.collidable and util.collide(destination, block.position):
					walled = True

			if not walled:
				self.oldLayer = self.layer
				self.layer -= 1
				self.layerChanging = True
				self.velocity.y = 0
				self.layerCooldown = 0.5
				self._oldResting = self.resting

	def toFront(self, game):
		if self.layerCooldown == 0 and self.layer < len(game.map.layers) - 1:
			walled = False
			destination = self.position.copy()
			destination.y += 69
			for block in self.getNearbyBlocks(self.layer + 1, destination, 1):
				if block.collidable and util.collide(destination, block.position):
					walled = True

			if not walled:
				self.oldLayer = self.layer
				self.layer += 1
				self.drawLayer = self.layer
				self.layerChanging = True
				self.velocity.y = 0
				self.layerCooldown = 0.5
				self._oldResting = self.resting

	def update(self, game, dt):
		last = self.position.copy()

		self.layerCooldown = max(0, self.layerCooldown - dt)

		if self.holdJump:
			if self.jumping:
				self.jumpTimer += 1
				self.velocity.y = util.approach(dt, self.velocity.y, self.jumpSpeed, 20)
				if self.jumpTimer == self.jumpTimerLimit:
					self.jumping = False
					self.jumpTimer = 0
			elif self.swimming:
				self.velocity.y = util.approach(dt, self.velocity.y, self.swimSpeed, 50)
		elif self.jumping:
			self.jumping = False

		if self.resting or self._oldResting:
			self.velocity.x = util.approach(dt, self.velocity.x, 0, 10)

			if self.velocity.x != 0 or self.layerChanging:
				self.particles.emit(game.dt * 0.001, self.layer)

		elif not self.layerChanging:
			self.velocity.y = util.approach(dt, self.velocity.y, self.map.gravity, 20)

		if self.swimming:
			self.velocity.x = util.approach(dt, self.velocity.x, 0, 5)
			self.bubbles.emit(game.dt * 0.001, self.layer)

		self.position.x += int(round(self.velocity.x * dt * self.speedModifier))
		self.position.y += int(round(self.velocity.y * dt * self.speedModifier))

		self.speedModifier = 1

		if self.position.x < 0:
			self.position.x = 0
			self.velocity.x = 0

		if self.position.right > game.map.width:
			self.position.right = game.map.width
			self.velocity.x = 0

		if self.position.y > game.map.height + 250:
			self.spawn()

		self.resting = False
		self.swimming = False

		if self.layerChanging:
			oldOff = self.layerOffset
			self.layerOffset = util.approach(dt, self.layerOffset, 70 * self.layer, 5)

			if self.layerOffset == oldOff:
				self.layerChanging = False
				self.velocity.y = self._oldAccel
				self.drawLayer = self.layer
				self._oldResting = False

			self.position.y += self.layerOffset - self._oldOff
		else:
			self._oldAccel = self.velocity.y

		self._oldOff = self.layerOffset

		for block in self.getNearbyBlocks(self.layer, self.position, 5):
			if util.collide(self.position, block.position):
				cell = block.position

				if block.collidable:
					siding = False

					if "l" in block.prop and self.position.right >= cell.left and last.right <= cell.left:
						self.position.right = cell.left
						siding = True
						if self.velocity.x > 0:
							self.velocity.x = 0

					if "r" in block.prop and self.position.left <= cell.right and last.left >= cell.right:
						self.position.left = cell.right
						siding = True
						if self.velocity.x < 0:
							self.velocity.x = 0

					if "u" in block.prop and self.position.bottom >= cell.top and last.bottom <= cell.top and not siding:
						self.position.bottom = cell.top
						self.resting = True
						if self.velocity.y > 0:
							self.velocity.y = 0

					if "d" in block.prop and self.position.top <= cell.bottom and last.top >= cell.bottom and not siding:
						self.position.top = cell.bottom
						if self.velocity.y < 0:
							self.velocity.y = 0

				if "s" in block.prop:
					self.speedModifier = 0.4

				if "w" in block.prop:
					self.swimming = True
					self.speedModifier = 0.5

				if "m" in block.prop:
					self.speedModifier = 0.2

				if "k" in block.prop:
					self.die()

	def draw(self, game):
		if self.drawShadow:
			shadowPos = self.genShadow(game)
			if shadowPos:
				game.screen.blit(self.shadow, shadowPos)

		self.particles.update(game, self.position.midleft)
		self.bubbles.update(game, self.position.midleft)

		self.animation.update(game.dt * 0.001)
		self.sprites.draw(game.screen)

	def setStatus(self, status):
		self.animation = status
		self.image = self.animation.getSplice()

	def genShadow(self, game):
		ground = self.getClosestGround(self.layer, self.position)
		pos = None
		
		if ground:
			if self.shadowPos:
				self.shadowPos.x = self.rect.centerx - self.shadow.get_width() / 2

				target = ground.rect.top
				stepToggle = False

				if self.layerChanging:
					if ground.rect.top < self._oldGround.rect.top and self.oldLayer < self.layer and self.shadowLooking:
						self.shadowPos.y = ground.rect.top - self.map.tilemap.tileheight
						self.shadowLooking = False

					if ground.rect.top > self._oldGround.rect.top and self.oldLayer > self.layer and self.shadowLooking:
						target = self._oldGround.rect.top - self.map.tilemap.tileheight
						stepToggle = True
						if self.shadowPos.y == target:
							target = ground.rect.top - self.map.tilemap.tileheight
							self.shadowLooking = False
				else:
					self._oldGround = ground
					self.shadowLooking = True

				if stepToggle:
					step = 2.5
				else:
					step = abs(target - self.shadowPos.y) * 0.3
					if step < 7:
						step = 7

				self.shadowPos.y = util.approach(game.dt * 0.001, self.shadowPos.y, target, step)

				pos = (self.shadowPos.x, self.shadowPos.y - self.shadow.get_height() / 2)

			else:
				self.shadowPos = Vector(self.rect.centerx - self.shadow.get_width() / 2, ground.rect.top)
				pos = (self.shadowPos.x, self.shadowPos.y - self.shadow.get_height() / 2)

		return pos

	def getClosestGround(self, layer, position):
		left = None
		right = None

		for i in xrange(position.bottom / self.map.tilemap.tileheight, self.map.tilemap.height):
			if (layer, position.centerx / self.map.tilemap.tilewidth, i) in self.map.blocks:
				block = self.map.blocks[(layer, position.centerx / self.map.tilemap.tilewidth, i)]
				blockAbove = None
				if (layer, position.centerx / self.map.tilemap.tilewidth, i - 1) in self.map.blocks:
					blockAbove = self.map.blocks[(layer, position.centerx / self.map.tilemap.tilewidth, i - 1)]

				if block.collidable or (block.liquid and blockAbove and not self.map.blocks[(layer, position.centerx / self.map.tilemap.tilewidth, i - 1)].liquid):
					return block

	def getNearbyBlocks(self, layer, position, tileRadius):
		d = []

		for i in xrange(tileRadius * 2 + 1):
			for j in xrange(tileRadius * 2 + 1):
				if (layer, position.centerx / self.map.tilemap.tilewidth + i - tileRadius, position.centery / self.map.tilemap.tileheight + j - tileRadius) in self.map.blocks:
					d.append(self.map.blocks[(layer, position.centerx / self.map.tilemap.tilewidth + i - tileRadius, position.centery / self.map.tilemap.tileheight + j - tileRadius)])

		return d
