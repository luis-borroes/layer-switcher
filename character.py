import pygame, utils, animation, particles, os

from vector import Vec2d as Vector
util = utils.Utils()

class Character(pygame.sprite.Sprite):
	def __init__(self, game, gMap, charType, pos, layer):
		self.sprites = pygame.sprite.Group()
		super(Character, self).__init__(self.sprites)

		self.map = gMap
		self.type = charType

		self.animList = {}
		for anim in os.listdir("assets/characters/%s" % self.type):
			info = anim[:anim.find(".")].split("+")
			if len(info) < 3:
				info[1:2] = [1, 1]

			self.animList[info[0]] = animation.Animation("assets/characters/%s/%s" % (self.type, anim), 50, 50, float(info[1]), float(info[2]))

		self.setStatus("standingRight")
		self.shadow = pygame.image.load("assets/sprites/shadow.png")
		self.drawShadow = True

		self.particles = particles.Particles(50, 0.5, (0, 0, 0, 50), (0, 0), (self.image.get_width(), self.map.tilemap.tileheight))
		self.bubbles = particles.Particles(50, 0.5, (0, 0, 255, 50), (0, 0), (self.image.get_width(), self.map.tilemap.tileheight))

		self.startPos = pos + (self.map.tilemap.tilewidth / 2 - self.image.get_width() / 2, -self.image.get_height() + self.map.tilemap.tileheight)
		self.startLayer = layer

		if self.type == "player":
			self.startPos.x += self.map.pPosition.x
			self.startPos.y += self.map.pPosition.y 

			self.startLayer = self.map.pLayer

		self.layerOffset = 70 * self.startLayer

		self.moveSpeed = 500
		self.jumpSpeed = -600
		self.jumpTimerLimit = 0.34
		self.swimSpeed = -400

		if hasattr(self.map.tilemap, "shadow"):
			self.drawShadow = bool(int(self.map.tilemap.shadow))

		self.spawn()

	def spawn(self):
		self.rect = pygame.rect.Rect((0, 0), self.image.get_size())
		self.position = pygame.rect.Rect(self.startPos, self.image.get_size())
		self.realPosition = self.position
		self.velocity = Vector(0, 0)
		self.direction = "Right"
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
		self._oldGround = self.getClosestGround(self.layer, self.position)
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

			self.setStatus("jumping" + self.direction, lambda: self.setStatus("falling" + self.direction))

	def moveLeft(self, dt):
		self.velocity.x = util.approach(dt, self.velocity.x, -self.moveSpeed, 20)
		self.direction = "Left"
		if self.resting:
			self.setStatus("walking" + self.direction)

	def moveRight(self, dt):
		self.velocity.x = util.approach(dt, self.velocity.x, self.moveSpeed, 20)
		self.direction = "Right"
		if self.resting:
			self.setStatus("walking" + self.direction)

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
				self.jumpTimer = min(self.jumpTimerLimit, self.jumpTimer + dt)
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

		self.realPosition = self.velocity * dt * self.speedModifier

		self.position.x += int(round(self.realPosition.x))
		self.position.y += int(round(self.realPosition.y))

		self.speedModifier = 1

		if self.position.x < 0:
			self.position.x = 0
			self.velocity.x = 0

		if self.position.right > game.map.width:
			self.position.right = game.map.width
			self.velocity.x = 0

		if self.position.y > game.map.height + 250:
			self.die()

		self.resting = False
		self.swimming = False

		if self.layerChanging:
			if self.layer > self.oldLayer:
				self.setStatus("switchFront", lambda: self.setStatus("falling" + self.direction))
			if self.layer < self.oldLayer:
				self.setStatus("switchBack", lambda: self.setStatus("falling" + self.direction))

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

		if self.resting:
			self.setStatus("standing" + self.direction)
		elif not self.jumping:
			self.setStatus("falling" + self.direction)

	def setStatus(self, status, callback = None):
		if status in self.animList:
			self.animation = self.animList[status]

			if callback:
				self.animation.setCallback(callback)

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
