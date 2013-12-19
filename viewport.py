import pygame

from vector import Vec2d as Vector

class Viewport(object):

	def __init__(self, game, x, y):
		self.position = Vector(x, y)
		self.rect = pygame.rect.Rect(self.position - (640, 360), (1280, 720))
		self.update(game, x, y)

	def update(self, game, x, y):
		vec = Vector(x - self.position.x, y - self.position.y) * 0.05
		if vec.length < 0.05:
			vec = Vector(0, 0)
		self.position += vec
		self.rect = pygame.rect.Rect(self.position - (640, 360), (1280, 720))

		if self.rect.x < 0:
			self.rect.x = 0

		if self.rect.x > game.map.width - 1280:
			self.rect.x = game.map.width - 1280

		if self.rect.y < 0:
			self.rect.y = 0

		if self.rect.y > game.map.height - 720:
			self.rect.y = game.map.height - 720

		game.player.rect.x = game.player.position.x - self.rect.x
		game.player.rect.y = game.player.position.y - self.rect.y

		for layer in game.map.layers:
			for block in layer:
				block.rect.x = block.x - self.rect.x
				block.rect.y = block.y - self.rect.y

		for deco in game.map.decorations:
			for block in deco:
				block.rect.x = block.x - self.rect.x
				block.rect.y = block.y - self.rect.y
