import pygame, block

from pytmx import tmxloader

class Mapper(object):

	def __init__(self, game, mapname):
		self.layers = []
		self.layerInfo = []
		self.decorations = []
		self.blocks = []
		self.map = tmxloader.load_pygame("maps/%s/map.tmx" % (mapname), pixelalpha = True)
		self.background = pygame.image.load("maps/%s/bg.png" % (mapname)).convert_alpha()
		self.bgSize = self.background.get_size()
		self.bgOffset = (0, 0)
		self.bgColor = (82, 246, 255)
		self.width = self.map.width * self.map.tilewidth
		self.height = self.map.height * self.map.tileheight
		self.layerID = -1

		if hasattr(self.map, "rgb"):
			self.bgColor = tuple([map(int, self.map.rgb.split())])

		for layer in self.map.getTileLayerOrder():
			self.layerID += 1
			if layer.visible:
				self.blocks.append([])
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
						self.blocks[self.layerID].append([])
						for height in xrange(0, self.map.height):
							img = self.map.getTileImage(width, height, self.layerID)
							if img:
								self.blocks[self.layerID][width].append(block.Block(width, height, self.map, img, self.layerID, self.layers[len(self.layers) - 1]))
							else:
								self.blocks[self.layerID][width].append(None)

	def updateAll(self, game):
		for layer in self.layers:
			layer.update(game.dt * 0.001)

		for deco in self.decorations:
			deco.update(game.dt * 0.001)

	def drawBackground(self, game):
		game.screen.blit(self.background, self.bgOffset)

	def drawLayer(self, game, layer):
		self.layers[layer].draw(game.screen)

	def drawDecos(self, game):
		for deco in self.decorations:
			deco.draw(game.screen)
