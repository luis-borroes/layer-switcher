import pygame

from vector import Vec2d as Vector
from utils import Utils
util = Utils()

class Viewport(object):

	def __init__(self, game, x, y):
		self.position = Vector(x - 640, y - 360)
		self.update(game, x, y)

	def update(self, game, x, y):
		vec = Vector(x - self.position.x, y - self.position.y)
		self.position = Vector(x - 640, y - 360)

		game.player.rect.x = game.player.position.x - self.position.x
		game.player.rect.y = game.player.position.y - self.position.y

		for layer in game.map.layers:
			for block in layer:
				block.rect.x = block.x - self.position.x
				block.rect.y = block.y - self.position.y

		for deco in game.map.decorations:
			for block in deco:
				block.rect.x = block.x - self.position.x
				block.rect.y = block.y - self.position.y

		"""if x < game.player.screenPos.x:
			game.player.rect.x = game.player.screenPos.x + (x - game.player.screenPos.x)
			x = game.player.screenPos.x

		if y > game.map.height - 420 - game.player.layerOffset:
			game.player.rect.y = y - game.player.screenPos.y - game.player.rect.height / 2 + game.player.layerOffset
			y = game.map.height - 420 - game.player.layerOffset"""

		if game.player.layerChanging:
			oldOff = game.player.layerOffset
			game.player.layerOffset = util.approach(game.dt / 1000., game.player.layerOffset, 70 * game.player.layer, 10)
			if game.player.layerOffset == oldOff:
				game.player.layerChanging = False
				game.player.resting = False
				game.player.acceleration.y = game.player.oldAccel
