import pygame, player, mapc, vector

class Game(object):
	def __init__(self, objScreen, objClock, fps):
		self.blnRunning = True
		self.paused = False

		self.map = mapc.Map("maps/main.tmx")

		self.pSprites = pygame.sprite.Group()
		self.player = player.Player(self.map, self.pSprites)
		self.layerOffset = 0
		self.offset = vector.Vec2d(self.player.screenPos.x - self.player.position.x, self.player.screenPos.y - self.player.position.y - self.layerOffset)

		while self.blnRunning:
			dt = objClock.tick(fps)
			pygame.display.set_caption("pyg %.2f FPS" % (objClock.get_fps()), "pyg")

			if dt > (1 / fps * 1000) + 10:
				dt = (1 / fps * 1000) + 10

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
						self.player.layerChanging = True

					elif event.key == pygame.K_s:
						self.player.layer = min(len(self.map.layers) - 1, self.player.layer + 1)
						self.player.layerChanging = True

			objScreen.fill((82, 246, 255))

			if not self.paused:
				self.pSprites.update(dt / 1000., self)

				self.viewport(dt / 1000., self.player.position.x, self.player.position.y)

				for layer in self.map.layers:
					layer.update(dt / 1000., self.offset, self.layerOffset)
					layer.draw(objScreen)
			else:
				for layer in self.map.layers:
					layer.draw(objScreen)

			self.pSprites.draw(objScreen)

			pygame.display.flip()

	def viewport(self, dt, x, y):
		if self.player.layerChanging:
			oldOff = self.layerOffset
			self.layerOffset = self.player._approach_(dt, self.layerOffset, 70 * self.player.layer, 10)
			if self.layerOffset == oldOff:
				self.player.layerChanging = False

		self.offset = vector.Vec2d(self.player.screenPos.x - x, self.player.screenPos.y - y - self.layerOffset)

	def leave(self):
		self.blnRunning = False
		pygame.quit()
