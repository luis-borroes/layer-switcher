import pygame, player, mapc, vector

class Game(object):
	def __init__(self, objScreen, objClock):
		self.blnRunning = True

		self.map = mapc.Map("maps/main.tmx")

		self.pSprites = pygame.sprite.Group()
		self.player = player.Player(self.map, self.pSprites)
		self.offset = vector.Vec2d(self.player.rect.x - self.player.position.x, self.player.rect.y - self.player.position.y)

		while self.blnRunning:
			dt = objClock.tick(60)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.leave()
					return

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.leave()
						return

					elif event.key == pygame.K_w:
						self.player.layer = max(1, self.player.layer - 1)

					elif event.key == pygame.K_s:
						self.player.layer = min(len(self.map.layers), self.player.layer + 1)

			objScreen.fill((82, 246, 255))

			self.pSprites.update(dt / 1000., self)

			self.offset = vector.Vec2d(self.player.rect.x - self.player.position.x, self.player.rect.y - self.player.position.y)

			for layer in self.map.layers:
				layer.update(dt / 1000., self.offset)
				layer.draw(objScreen)

			self.pSprites.draw(objScreen)

			pygame.display.flip()

	def leave(self):
		self.blnRunning = False
		pygame.quit()