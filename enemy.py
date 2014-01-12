import pygame, character

from vector import Vec2d as Vector

class Enemy(character.Character):
	group = []

	def __init__(self, game, gMap, pos, layer):
		super(Enemy, self).__init__(game, gMap, "enemy", pos, layer)

		self.inViewport = False

		Enemy.group.append(self)

	def spawn(self):
		super(Enemy, self).spawn()

		self.holdJump = True

	def die(self):
		self.spawn()

	def update(self, game, dt):
		self.inViewport = self.position.centerx in xrange(game.viewport.rect.left, game.viewport.rect.right) and self.position.centery in xrange(game.viewport.rect.top, game.viewport.rect.bottom)

		if self.inViewport and self.layer == game.player.layer:

			if game.player.position.centerx < self.position.centerx:
				self.moveLeft(dt)

			elif game.player.position.centerx > self.position.centerx:
				self.moveRight(dt)

			if game.player.position.centery < self.position.centery:
				self.jump()

		super(Enemy, self).update(game, dt)

	def draw(self, game):
		super(Enemy, self).draw(game)
