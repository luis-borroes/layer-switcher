import pygame, player, mapc, vector

class Game(object):
	def __init__(self, objScreen, objClock, fps):
		self.blnRunning = True
		self.paused = False

		self.map = mapc.Map("maps/main.tmx")

		self.pSprites = pygame.sprite.Group()
		self.player = player.Player(self.map, self.pSprites)
		self.offset = vector.Vec2d(self.player.rect.x - self.player.position.x, self.player.rect.y - self.player.position.y)

		while self.blnRunning:
			dt = objClock.tick(fps)
			pygame.display.set_caption("pyg %.2f FPS" % (objClock.get_fps()), "pyg")

			if dt/1000. > 1/fps:
				dt = 1/fps * 1000

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.leave()
					return

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.leave()
						return

					elif event.key == pygame.K_w:
						self.player.layer = max(0, self.player.layer - 1)

					elif event.key == pygame.K_s:
						self.player.layer = min(len(self.map.layers) - 1, self.player.layer + 1)	

			objScreen.fill((82, 246, 255))

			if not self.paused:
				self.pSprites.update(dt / 1000., self)

				self.viewport(self.player.position.x, self.player.position.y)

				for layer in self.map.layers:
					layer.update(dt / 1000., self.offset)
					layer.draw(objScreen)
			else:
				for layer in self.map.layers:
					layer.draw(objScreen)

			self.pSprites.draw(objScreen)

			pygame.display.flip()

	def viewport(self, x, y):
		self.offset = vector.Vec2d(self.player.rect.x - x, self.player.rect.y - y)

	def leave(self):
		self.blnRunning = False
		pygame.quit()