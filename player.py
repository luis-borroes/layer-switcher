import pygame, character, enemy, utils
util = utils.Utils()

from vector import Vec2d as Vector

class Player(character.Character):

	def __init__(self, game):
		super(Player, self).__init__(game, game.map, "player", Vector(0, 0), 0)

	def spawn(self):
		super(Player, self).spawn()

		self.spaced = False
		self.key_w = False
		self.key_s = False
		self.cdBar = pygame.rect.Rect((self.rect.left, self.rect.bottom + 2), (0, 10))

	def die(self, game):
		game.paused = True
		self.setStatus("death", lambda: self.realDie(game))

	def realDie(self, game):
		for gEnemy in enemy.Enemy.group:
			gEnemy.die(game)

		self.spawn()
		game.paused = False
		game.viewport.update(game, self.position.centerx, self.position.centery)

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

		for gEnemy in enemy.Enemy.group:
			if util.collide(self.position, gEnemy.position) and self.layer == gEnemy.layer:
				self.die(game)
				break

	def draw(self, game):
		super(Player, self).draw(game)

		if self.cdBar.width > 0:
			pygame.draw.rect(game.screen, (190, 0, 0), self.cdBar)
