import pygame, utils, animation, particles, os

from vector import Vec2d as Vector
util = utils.Utils()

class Character(object):
	def __init__(self, game, gMap, charType, pos, layer, defaultAnims = True):
		self.map = gMap
		self.type = charType
		self.defaultAnims = defaultAnims

		if self.defaultAnims:
			self.animList = {}
			for anim in os.listdir("assets/characters/%s" % self.type):
				info = anim[:anim.find(".")].split("+")
				if len(info) < 3:
					info[1:2] = [1, 1]

				self.animList[info[0]] = animation.Animation("assets/characters/%s/%s" % (self.type, anim), 50, 50, float(info[1]), int(info[2]))

		self.status = ""
		self.animation = None
		self._statusChanged = False
		self.setStatus("standingRight")
		self.shadow = pygame.image.load("assets/sprites/shadow.png").convert_alpha()

		self.particles = particles.Particles(50, 0.5, (0, 0, 0, 50), (0, 0), (self.image.get_width(), self.map.tilemap.tileheight))
		self.bubbles = particles.Particles(50, 0.5, (0, 0, 255, 50), (0, 0), (self.image.get_width(), self.map.tilemap.tileheight))

		self.startPos = pos + (self.map.tilemap.tilewidth * 0.5 - self.image.get_width() * 0.5, -self.image.get_height() + self.map.tilemap.tileheight)
		self.startLayer = layer

		if self.type == "player":
			self.startPos.x += self.map.pPosition.x
			self.startPos.y += self.map.pPosition.y 

			self.startLayer = self.map.pLayer

		self.layerOffset = 70 * self.startLayer

		self.moveSpeed = 600
		self.jumpSpeed = -750
		self.jumpTimerLimit = 0.34
		self.swimSpeed = -400

		self.moveAccel = 30
		self.jumpAccel = 20
		self.swimAccel = 50

		self.spawn()

	def spawn(self):
		self.rect = pygame.rect.Rect((0, 0), self.image.get_size())
		self.position = pygame.rect.Rect(self.startPos, self.image.get_size())
		self.realChange = Vector(0, 0)
		self.velocity = Vector(0, 0)
		self.direction = "Right"
		self.speedModifier = 1
		self.resting = False
		self.movingLeft = False
		self.movingRight = False
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
		self._oldResting = False
		self._oldPos = None
		self._oldNearbyPos = None
		self._oldGround = self.getClosestGround(self.layer, self.position)
		self._oldNearby = []
		self.shadowPos = None
		self.shadowLooking = True
		self.isDead = False

	def die(self, game):
		self.isDead = True
		pass

	def jump(self):
		if not self.layerChanging and not self.jumping and not self.swimming and self.resting:
			self.jumping = True
			self.velocity.y = self.jumpSpeed
			self.resting = False

			self.setStatus("jumping" + self.direction, lambda: self.setStatus("falling" + self.direction))

	def moveLeft(self, dt):
		self.velocity.x = util.approach(dt, self.velocity.x, -self.moveSpeed, self.moveAccel)
		self.direction = "Left"
		if self.resting:
			self.setStatus("walking" + self.direction)

	def moveRight(self, dt):
		self.velocity.x = util.approach(dt, self.velocity.x, self.moveSpeed, self.moveAccel)
		self.direction = "Right"
		if self.resting:
			self.setStatus("walking" + self.direction)

	def toBack(self, game):
		if self.layerCooldown == 0 and self.layer > 0 and self.position.bottom > 0:
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
		if self.layerCooldown == 0 and self.layer < len(game.map.layers) - 1 and self.position.bottom > 0:
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

		if self.movingLeft:
			self.moveLeft(dt)

		if self.movingRight:
			self.moveRight(dt)

		if self.holdJump:
			if self.jumping:
				self.jumpTimer = min(self.jumpTimerLimit, self.jumpTimer + dt)
				self.velocity.y = util.approach(dt, self.velocity.y, self.jumpSpeed, self.jumpAccel)

				if self.jumpTimer == self.jumpTimerLimit:
					self.jumping = False
					self.jumpTimer = 0

			elif self.swimming:
				self.velocity.y = util.approach(dt, self.velocity.y, self.swimSpeed, self.swimAccel)

		elif self.jumping:
			self.jumping = False
			self.jumpTimer = 0

		if self.resting or self._oldResting:
			self.velocity.x = util.approach(dt, self.velocity.x, 0, 10)

			if self.velocity.x != 0 or self.layerChanging:
				self.particles.emit(game.dt * 0.001, self.layer)

		elif not self.layerChanging:
			self.velocity.y = util.approach(dt, self.velocity.y, self.map.gravity, self.map.gravityAccel)

		if self.swimming:
			self.velocity.x = util.approach(dt, self.velocity.x, 0, 5)
			self.bubbles.emit(game.dt * 0.001, self.layer)

		self.realChange = self.velocity * dt * self.speedModifier

		self.position.x += int(round(self.realChange.x))
		self.position.y += int(round(self.realChange.y))

		self.speedModifier = 1

		if self.position.x < 0:
			self.position.x = 0
			if self.velocity.x < 0:
				self.velocity.x = 0

		if self.position.right > game.map.width:
			self.position.right = game.map.width
			if self.velocity.x > 0:
				self.velocity.x = 0

		if self.position.y > game.map.height + 250:
			self.die(game)

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

		for block in self.getNearbyBlocks(self.layer, self.position, 1):
			if util.collide(self.position, block.position):
				cell = block.position

				if block.collidable:
					if last.top < cell.bottom and last.bottom > cell.top:
						if "l" in block.prop and self.position.right >= cell.left and last.right <= cell.left:
							self.position.right = cell.left
							if self.velocity.x > 0:
								self.velocity.x = 0

						if "r" in block.prop and self.position.left <= cell.right and last.left >= cell.right:
							self.position.left = cell.right
							if self.velocity.x < 0:
								self.velocity.x = 0

					if last.left < cell.right and last.right > cell.left:
						if "u" in block.prop and self.position.bottom >= cell.top and last.bottom <= cell.top:
							self.position.bottom = cell.top
							self.resting = True
							if self.velocity.y > 0:
								self.velocity.y = 0

						if "d" in block.prop and self.position.top <= cell.bottom and last.top >= cell.bottom:
							self.position.top = cell.bottom
							if self.velocity.y < 0:
								self.velocity.y = 0

				if self.type == "player" and "keyhole" in block.prop and not block.hooked:
					if (block.tilex, block.tiley + 1) in self.map.layers[self.layer].blocks and "keyhole" in self.map.layers[self.layer].blocks[(block.tilex, block.tiley + 1)].prop:
						self._keyTarget.append(self.map.layers[self.layer].blocks[(block.tilex, block.tiley + 1)])
					else:
						self._keyTarget.append(block)

				if "s" in block.prop:
					self.speedModifier = 0.4

				if "w" in block.prop:
					self.swimming = True
					self.speedModifier = 0.5

				if "m" in block.prop:
					self.speedModifier = 0.2

				if "k" in block.prop:
					self.die(game)

		if not game.paused:
			if not self.layerChanging and not self.jumping:
				if self.resting:
					if not self.movingRight and not self.movingLeft:
						self.setStatus("standing" + self.direction)

				elif not self.status in ("jumpingLeft", "jumpingRight"):
					self.setStatus("falling" + self.direction)

		self._statusChanged = False
		self.movingRight = False
		self.movingLeft = False

	def draw(self, game):
		if self.map.drawShadow:
			self.genShadow(game)
			if self.shadowPos:
				game.screen.blit(self.shadow, self.shadowPos)

		self.particles.update(game, self.position.midleft)
		self.bubbles.update(game, self.position.midleft)

		if self.defaultAnims and (not game.paused or self.isDead):
			self.animation.update(game.dt * 0.001)

		game.screen.blit(self.image, (self.position.x - game.viewport.rect.x, self.position.y - game.viewport.rect.y))

	def setStatus(self, status, callback = None):
		if self.defaultAnims:
			if not self._statusChanged and status != self.status and status in self.animList:
				self._statusChanged = True

				if self.animation:
					self.animation.frame = 0

				self.animation = self.animList[status]
				self.status = status

				if callback:
					self.animation.setCallback(callback)

				self.image = self.animation.getSplice()

	def genShadow(self, game):
		ground = self.getClosestGround(self.layer, self.position)

		if ground:
			if self.shadowPos:
				self.shadowPos.x = self.rect.centerx - self.shadow.get_width() * 0.5

				target = ground.position.top - game.viewport.rect.top - self.map.tilemap.tileheight * 0.5
				stepToggle = False

				if self.layerChanging:
					if ground.position.top < self._oldGround.position.top and self.oldLayer < self.layer and self.shadowLooking:
						self.shadowPos.y = ground.position.top - game.viewport.rect.top - self.map.tilemap.tileheight - self.map.tilemap.tileheight * 0.5
						self.shadowLooking = False

					if ground.position.top > self._oldGround.position.top and self.oldLayer > self.layer and self.shadowLooking:
						target = self._oldGround.position.top - game.viewport.rect.top - self.map.tilemap.tileheight - self.map.tilemap.tileheight * 0.5
						stepToggle = True
						
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

			else:
				self.shadowPos = Vector(self.rect.centerx - self.shadow.get_width() * 0.5, ground.position.top - game.viewport.rect.top - self.shadow.get_height() * 0.5)

		else:
			self.shadowPos = None

	def getClosestGround(self, layer, position):
		if (position.centerx / self.map.tilemap.tilewidth, position.centery / self.map.tilemap.tileheight) == self._oldPos and layer == self.oldLayer:
			return self._oldGround

		else:
			for ground in self.map.layers[layer].grounds[position.centerx / self.map.tilemap.tilewidth]:
				if position.y <= ground.y or (self.layerChanging and util.collide(position, ground.position)):
					self._oldPos = (position.centerx / self.map.tilemap.tilewidth, position.centery / self.map.tilemap.tileheight)

					return ground

	def getNearbyBlocks(self, layer, position, tileRadius):
		d = []

		if (position.centerx / self.map.tilemap.tilewidth, position.centery / self.map.tilemap.tileheight) == self._oldNearbyPos and self._oldNearby != []:
			return self._oldNearby

		else:
			for i in xrange(tileRadius * 2 + 1):
				for j in xrange(tileRadius * 2 + 1):
					if (position.centerx / self.map.tilemap.tilewidth + i - tileRadius, position.centery / self.map.tilemap.tileheight + j - tileRadius) in self.map.layers[layer].blocks:
						d.append(self.map.layers[layer].blocks[(position.centerx / self.map.tilemap.tilewidth + i - tileRadius, position.centery / self.map.tilemap.tileheight + j - tileRadius)])

			self._oldNearbyPos = (position.centerx / self.map.tilemap.tilewidth, position.centery / self.map.tilemap.tileheight)
			self._oldNearby = d

			return d
