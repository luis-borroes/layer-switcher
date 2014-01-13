import pygame, character

from vector import Vec2d as Vector

class Enemy(character.Character):
	group = []
	blue = "enemyBlue"
	yellow = "enemyYellow"
	red = "enemyRed"

	def __init__(self, game, gMap, enemyType, pos, layer):
		super(Enemy, self).__init__(game, gMap, enemyType, pos, layer)

		self.inProximity = False

		if self.type in [Enemy.yellow, Enemy.red]:
			self.moveSpeed = 400
			self.jumpSpeed = -400
			self.jumpTimerLimit = 0.25
			self.swimSpeed = -250

		Enemy.group.append(self)

	def spawn(self):
		super(Enemy, self).spawn()

	def die(self):
		self.spawn()

	def update(self, game, dt):
		in_x = self.position.centerx - game.player.position.centerx in xrange(-game.resolution[0] / 2, game.resolution[0] / 2)
		in_y = self.position.centery - game.player.position.centery in xrange(-game.resolution[1] / 2, game.resolution[1] / 2)
		self.inProximity = in_x and in_y

		if self.type == Enemy.blue:
			if self.inProximity and self.layer == game.player.layer:

				if game.player.position.centerx < self.position.centerx:
					self.moveLeft(dt)

				elif game.player.position.centerx > self.position.centerx:
					self.moveRight(dt)

				if game.player.position.centery < self.position.centery:
					self.holdJump = True

					if self.resting:
						self.jump()

				if game.player.position.centery > self.position.centery and self.holdJump:
					self.holdJump = False

		if self.type == Enemy.yellow:
			if self.inProximity:

				if game.player.position.centerx < self.position.centerx:
					self.moveLeft(dt)

				elif game.player.position.centerx > self.position.centerx:
					self.moveRight(dt)

				if game.player.position.centery < self.position.centery:
					self.holdJump = True

					if self.resting:
						self.jump()

				if game.player.position.centery > self.position.centery and self.holdJump:
					self.holdJump = False

		if self.type == Enemy.red:
			if self.inProximity:

				if game.player.layer > self.layer:
					self.toFront(game)
				elif game.player.layer < self.layer:
					self.toBack(game)

				if game.player.position.centerx < self.position.centerx:
					self.moveLeft(dt)

				elif game.player.position.centerx > self.position.centerx:
					self.moveRight(dt)

				if game.player.position.centery < self.position.centery:
					self.holdJump = True

					if self.resting:
						self.jump()

				if game.player.position.centery > self.position.centery and self.holdJump:
					self.holdJump = False

		super(Enemy, self).update(game, dt)

	def draw(self, game):
		super(Enemy, self).draw(game)
