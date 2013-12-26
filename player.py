import pygame, character

from vector import Vec2d as Vector
from utils import Utils
util = Utils()

class Player(character.Character):

	def __init__(self, objMap):
		super(Player, self).__init__(objMap, "player", Vector(0, 0), 0)

		for obj in objMap.map.getObjects():
			if obj.name == "spawn":
				self.position.x = obj.x + (objMap.map.tilewidth / 2 - self.image.get_width() / 2)
				self.position.y = obj.y - (self.image.get_height() - objMap.map.tileheight)
				if hasattr(obj, "layer"):
					self.layer = int(obj.layer)
					self.drawLayer = self.layer

		self.startPos = self.position.topleft
		self.startLayer = self.layer

	def spawn(self):
		super(Player, self).spawn()

		self.spaced = False
		self.key_w = False
		self.key_s = False
		self.cdBar = pygame.rect.Rect((self.rect.left, self.rect.bottom + 2), (0, 10))

	def die(self):
		self.spawn()

	def update(self, game, dt):
		if self.key_w:
			self.key_w = False
			self.toBack(game)

		if self.key_s:
			self.key_s = False
			self.toFront(game)

		keys = pygame.key.get_pressed()

		if keys[pygame.K_a]:
			self.moveLeft(dt)

		if keys[pygame.K_d]:
			self.moveRight(dt)

		if self.spaced:
			self.spaced = False
			self.jump()

		self.holdJump = keys[pygame.K_SPACE]

		super(Player, self).update(game, dt)

	def draw(self, screen):
		super(Player, self).draw(screen)

		if self.cdBar.width > 0:
			pygame.draw.rect(screen, (190, 0, 0), self.cdBar)
