import pygame, vector, enemy, item, layer

from pytmx import tmxloader

class Mapper(object):

	def __init__(self, game, world, mapName):
		self.mapName = mapName
		self.world = world

		self.drawable = []
		self.layers = []

		self.tilemap = tmxloader.load_pygame("maps/%s/%s/map.tmx" % (self.world, self.mapName), pixelalpha = True)
		self.width = self.tilemap.width * self.tilemap.tilewidth
		self.height = self.tilemap.height * self.tilemap.tileheight

		self.drawShadow = True
		self.gravity = 750
		self.gravityAccel = 25
		self.bgColor = (82, 246, 255)
		self.background = None

		self.pPosition = vector.Vec2d(0, 0)
		self.pLayer = 0

		self.layerCount = -1
		self.hasKeyHoles = False

		if hasattr(self.tilemap, "shadow"):
			self.drawShadow = bool(int(self.tilemap.shadow))

		if hasattr(self.tilemap, "gravity"):
			self.gravity = int(self.tilemap.gravity)

		if hasattr(self.tilemap, "gravityAccel"):
			self.gravityAccel = int(self.tilemap.gravityAccel)

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

		for rawLayer in self.tilemap.getTileLayerOrder():
			self.layerCount += 1

			if rawLayer.visible:
				layer.Layer(self, rawLayer)
					
		self.layerCount += 1

		MapText.group = []
		for i in self.layers:
			MapText.group.append([])

		for obj in self.tilemap.getObjects():
			if obj.name == "spawn":
				self.pPosition.x = obj.x
				self.pPosition.y = obj.y
				if hasattr(obj, "layer"):
					self.pLayer = int(obj.layer)

			elif obj.name == "enemy":
				eLayer = 0
				enemyType = "enemyBlue"

				if hasattr(obj, "layer"):
					eLayer = int(obj.layer)

				if hasattr(obj, "color"):
					enemyType = "enemy" + obj.color.capitalize()

				enemy.Enemy(game, self, enemyType, vector.Vec2d(obj.x, obj.y), eLayer)

			elif obj.name == "item":
				iLayer = 0
				itemType = "keyYellow"

				if hasattr(obj, "layer"):
					iLayer = int(obj.layer)

				if hasattr(obj, "color"):
					itemType = "key" + obj.color.capitalize()

				item.Item(game, self, itemType, vector.Vec2d(obj.x, obj.y), iLayer)

			elif obj.name == "text":
				text = ""
				tLayer = 0

				if hasattr(obj, "text"):
					text = obj.text

				if hasattr(obj, "layer"):
					tLayer = int(obj.layer)

				MapText(game, text, tLayer, vector.Vec2d(obj.x, obj.y), obj.width)

	def drawBackground(self, game):
		if self.background:
			game.screen.blit(self.background, self.bgOffset)

class MapText(object):
	group = []

	def __init__(self, game, text, tLayer, pos, width):
		self.text = text
		self.pos = pos

		MapText.group[tLayer].append(self)

		words = text.split()
		line = ""
		lines = []
		lineCount = 0

		for word in words:
			size = game.smallFont.size(line + word)

			if size[0] >= width:
				lines.append(line.strip())

				line = ""
				lineCount += 1

			line += word + " "

		lines.append(line.strip())
		lineCount += 1

		self.surface = pygame.Surface((width, (size[1] + 5) * lineCount), pygame.SRCALPHA | pygame.HWSURFACE)

		for i in xrange(lineCount):
			self.surface.blit(game.smallFont.render(lines[i], 1, (0, 0, 0)), (0, (size[1] + 5) * i))

	def draw(self, game):
		game.screen.blit(self.surface, self.pos - game.viewport.rect.topleft)
