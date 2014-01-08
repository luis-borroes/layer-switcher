import pygame, block

from pytmx import tmxloader

class Mapper(object):

	def __init__(self, game, world, mapName):
		self.layers = []
		self.layerInfo = []
		self.totalLayers = []
		self.blocks = {}
		self.mapName = mapName
		self.world = world
		self.tilemap = tmxloader.load_pygame("maps/%s/%s/map.tmx" % (self.world, self.mapName), pixelalpha = True)
		self.gravity = 600
		self.bgColor = (82, 246, 255)
		self.width = self.tilemap.width * self.tilemap.tilewidth
		self.height = self.tilemap.height * self.tilemap.tileheight
		self.layerCount = -1
		self.background = None

		if hasattr(self.tilemap, "gravity"):
			self.gravity = int(self.tilemap.gravity)

		if hasattr(self.tilemap, "rgb"):
			self.bgColor = tuple([map(int, self.tilemap.rgb.split())])

		if hasattr(self.tilemap, "bg"):
			tmp = self.tilemap.bg.split(":")
			if tmp[0] == "d":
				self.background = pygame.image.load("assets/sprites/backgrounds/%s.png" % (tmp[1])).convert_alpha()
			elif tmp[0] == "c":
				self.background = pygame.image.load("maps/%s/%s/%s.png" % (self.world, self.mapName, tmp[1])).convert_alpha()

			self.bgSize = self.background.get_size()
			self.bgOffset = (0, 0)

		for layer in self.tilemap.getTileLayerOrder():
			self.layerCount += 1

			if layer.visible:
				if hasattr(layer, "decorations"):
					self.totalLayers.append(pygame.sprite.Group())

					for x in xrange(0, self.tilemap.width):
						for y in xrange(0, self.tilemap.height):
							img = self.tilemap.getTileImage(x, y, self.layerCount)

							if img:
								block.Block(x, y, self.tilemap, img, self.layerCount, self.totalLayers[self.layerCount])

				else:
					newGroup = pygame.sprite.Group()
					self.layers.append(newGroup)
					self.totalLayers.append(newGroup)
					self.layerInfo.append(layer)

					for x in xrange(0, self.tilemap.width):
						for y in xrange(0, self.tilemap.height):
							img = self.tilemap.getTileImage(x, y, self.layerCount)
							
							if img:
								self.blocks[(len(self.layers) - 1, x, y)] = block.Block(x, y, self.tilemap, img, self.layerCount, self.totalLayers[self.layerCount])

	def updateAll(self, game):
		for layer in self.totalLayers:
			layer.update(game.dt * 0.001)

	def drawBackground(self, game):
		if self.background:
			game.screen.blit(self.background, self.bgOffset)
