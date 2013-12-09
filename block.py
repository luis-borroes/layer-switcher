import pygame

from vector import Vec2d as Vector

class Block(pygame.sprite.Sprite):

	def __init__(self, x, y, objMap, img, layers, *groups):
		super(Block, self).__init__(*groups)

		self.image = img
		self.x = x * objMap.tilewidth
		self.y = y * objMap.tileheight

		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y

		self.position = self.rect.copy()

		self.prop = objMap.getTileProperties((x, y, len(layers) - 1)) or {}

	def update(self, dt, offset):
		self.rect.x = self.x + offset.x
		self.rect.y = self.y + offset.y