import pygame, block

from pytmx import tmxloader

class Mapper(object):

	def __init__(self, game, mapname):
		self.layers = []
		self.layerInfo = []
		self.decorations = []
		self.blocks = {}
		self.tilemap = tmxloader.load_pygame("maps/%s/map.tmx" % (mapname), pixelalpha = True)
		self.background = pygame.image.load("maps/%s/bg.png" % (mapname)).convert_alpha()
		self.bgSize = self.background.get_size()
		self.bgOffset = (0, 0)
		self.bgColor = (82, 246, 255)
		self.width = self.tilemap.width * self.tilemap.tilewidth
		self.height = self.tilemap.height * self.tilemap.tileheight
		self.layerID = -1

		if hasattr(self.tilemap, "rgb"):
			self.bgColor = tuple([map(int, self.tilemap.rgb.split())])

		for layer in self.tilemap.getTileLayerOrder():
			self.layerID += 1

			if layer.visible:
				if hasattr(layer, "decorations"):
					self.decorations.append(pygame.sprite.Group())

					for x in xrange(0, self.tilemap.width):
						for y in xrange(0, self.tilemap.height):
							img = self.tilemap.getTileImage(x, y, self.layerID)

							if img:
								block.Block(x, y, self.tilemap, img, self.layerID, self.decorations[len(self.decorations) - 1])

				else:
					self.layers.append(pygame.sprite.Group())
					self.layerInfo.append(layer)

					for x in xrange(0, self.tilemap.width):
						for y in xrange(0, self.tilemap.height):
							img = self.tilemap.getTileImage(x, y, self.layerID)
							
							if img:
								self.blocks[(len(self.layers) - 1, x, y)] = block.Block(x, y, self.tilemap, img, self.layerID, self.layers[len(self.layers) - 1])

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
