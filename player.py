import pygame, character, enemy, item

from vector import Vec2d as Vector

class Player(character.Character):

	def __init__(self, game):
		super(Player, self).__init__(game, game.map, "player", Vector(0, 0), 0)

	def spawn(self):
		super(Player, self).spawn()

		self.keyRect = self.position.inflate(15, 5)
		self.keyList = []
		self.keyNames = []

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

		for gItem in item.Item.group:
			gItem.spawn()

		for keyHole in self.map.keyHoles:
			keyHole.hooked = False

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
			self.holdJump = True
			self.jump()

		self._keyTarget = []

		super(Player, self).update(game, dt)

		self.keyRect.centerx = self.position.centerx
		self.keyRect.bottom = self.position.bottom

		self.key()

	def draw(self, game):
		super(Player, self).draw(game)

		if self.cdBar.width > 0:
			pygame.draw.rect(game.screen, (190, 0, 0), self.cdBar)

	def key(self):
		for keyHole in self._keyTarget:
			if "key" + keyHole.prop["keyhole"].capitalize() in self.keyNames:
				index = self.keyNames.index("key" + keyHole.prop["keyhole"].capitalize())
				key = self.keyList[index]

				key.hook = keyHole.position
				key.hookType = "block"
				key.hookBlock = keyHole

				keyHole.hooked = True

				self.keyNames.pop(index)
				self.keyList.pop(index)

				for trailing in xrange(index, index + len(self.keyList[index:])):
					trailKey = self.keyList[trailing]
					if trailing != 0:
						trailKey.hook = self.keyList[trailing - 1].position
						trailKey.hookType = "player"
					else:
						trailKey.hook = self.keyRect
						trailKey.hookType = "player"
