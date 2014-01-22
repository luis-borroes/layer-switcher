import pygame

from vector import Vec2d as Vector

class Block(pygame.sprite.Sprite):

	def __init__(self, x, y, objMap, img, layer, *groups):
		super(Block, self).__init__(*groups)

		self.image = img
		self.tilex = x
		self.tiley = y

		self.x = x * objMap.tilewidth
		self.y = y * objMap.tileheight

		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y

		self.position = self.rect.copy()

		self.prop = objMap.getTileProperties((x, y, layer)) or {}
		self.collidable = "l" in self.prop or "r" in self.prop or "u" in self.prop or "d" in self.prop or "c" in self.prop
		self.liquid = "w" in self.prop or "m" in self.prop
		self.hooked = False
		self.done = False
