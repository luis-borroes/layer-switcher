import pygame, block

from pytmx import tmxloader

class Map(object):

	def __init__(self, filename):
		self.layers = []
		self.layerInfo = []
		self.map = tmxloader.load_pygame(filename, pixelalpha = True)

		for layer in self.map.getTileLayerOrder():
			if layer.visible:
				self.layers.append(pygame.sprite.Group())
				self.layerInfo.append(layer)
				for width in xrange(0, self.map.width):
					for height in xrange(0, self.map.height):
						img = self.map.getTileImage(width, height, len(self.layers) - 1)
						if img:
							block.Block(width, height, self.map, img, self.layers, self.layers[len(self.layers) - 1])