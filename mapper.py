import pygame, block

from pytmx import tmxloader

class Mapper(object):

	def __init__(self, filename):
		self.layers = []
		self.layerInfo = []
		self.decorations = []
		self.map = tmxloader.load_pygame(filename, pixelalpha = True)
		self.width = self.map.width * self.map.tilewidth
		self.height = self.map.height * self.map.tileheight
		self.layerID = -1

		for layer in self.map.getTileLayerOrder():
			self.layerID += 1
			if layer.visible:
				if hasattr(layer, "decorations"):
					self.decorations.append(pygame.sprite.Group())
					for width in xrange(0, self.map.width):
						for height in xrange(0, self.map.height):
							img = self.map.getTileImage(width, height, self.layerID)
							if img:
								block.Block(width, height, self.map, img, self.layerID, self.decorations[len(self.decorations) - 1])
				else:
					self.layers.append(pygame.sprite.Group())
					self.layerInfo.append(layer)
					for width in xrange(0, self.map.width):
						for height in xrange(0, self.map.height):
							img = self.map.getTileImage(width, height, self.layerID)
							if img:
								block.Block(width, height, self.map, img, self.layerID, self.layers[len(self.layers) - 1])

	def updateAll(self, game):
		for layer in self.layers:
			layer.update(game.dt / 1000.)
		for deco in self.decorations:
			deco.update(game.dt / 1000.)

	def drawAll(self, game):
		for layer in self.layers:
			layer.draw(game.screen)
		for deco in self.decorations:
			deco.draw(game.screen)
