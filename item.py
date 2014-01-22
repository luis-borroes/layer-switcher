import pygame, character, utils

from vector import Vec2d as Vector
util = utils.Utils()

class Item(character.Character):
	group = []
	yellow = "keyYellow"
	green = "keyGreen"
	red = "keyRed"
	blue = "keyBlue"

	def __init__(self, game, gMap, itemType, pos, layer):
		self.type = itemType
		self.image = pygame.image.load("assets/sprites/%s.png" % self.type).convert_alpha()

		super(Item, self).__init__(game, gMap, itemType, pos, layer, False)

		Item.group.append(self)

	def spawn(self):
		super(Item, self).spawn()

		self.hook = None
		self.hookType = None
		self.hookBlock = None

	def update(self, game, dt):
		if self.hook:
			if not util.collide(self.position, self.hook) or self.position.bottom > self.hook.bottom or self.hookType != "player":
				if self.hookType == "block":
					oldCenterx = self.position.centerx
					oldBottom = self.position.bottom

					self.position.centerx = util.approach(dt, self.position.centerx, self.hook.centerx, 5)
					self.position.bottom = util.approach(dt, self.position.bottom, self.hook.bottom, 5)

					if self.position.centerx == oldCenterx and self.position.bottom == oldBottom:
						self.hookBlock.done = True

				elif self.hookType == "player":
					vec = Vector(self.hook.centerx - self.position.centerx, self.hook.bottom - self.position.bottom) * 0.005 * game.dt
					if vec.length < 0.05:
						vec = Vector(0, 0)

					self.position.x += vec.x
					self.position.y += vec.y

			else:
				super(Item, self).update(game, dt)

			if self.hookType == "player" and game.player.layerChanging:
				if game.player.oldLayer > game.player.layer:
					self.position.y -= 5 * dt * 100
				elif game.player.oldLayer < game.player.layer:
					self.position.y += 5 * dt * 100

			if self.hookType == "player" and self.layer != game.player.layer:
				self.layer = game.player.layer

			if self.hookType == "player" and self.drawLayer != game.player.drawLayer:
				self.drawLayer = game.player.drawLayer

			if self.hookType == "player" and self.oldLayer != game.player.oldLayer:
				self.oldLayer = game.player.oldLayer

		else:
			super(Item, self).update(game, dt)
