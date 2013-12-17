import pygame, player, mapper, vector, viewport

class Game(object):

	def __init__(self, objScreen, objClock, fps, font):
		self.blnRunning = True
		self.paused = False
		self.screen = objScreen
		self.font = font

		self.map = mapper.Map("maps/1-1.tmx")

		self.player = player.Player(self.map)
		self.viewport = viewport.Viewport(self, self.player.position.x, self.player.position.y)

		while self.blnRunning:
			self.dt = objClock.tick(fps)
			pygame.display.set_caption("pyg %.2f FPS" % (objClock.get_fps()), "pyg")

			if self.dt > (1 / fps * 1000) + 10:
				self.dt = (1 / fps * 1000) + 10
		
			oldLayer = self.player.layer

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

			if self.player.layer != oldLayer:
				self.player.layerChanging = True
				self.player.acceleration.y = 0

			self.screen.fill((82, 246, 255))

			if not self.paused:
				self.player.sprites.update(self.dt / 1000., self)
				self.map.updateAll(self)
				self.viewport.update(self, self.player.position.x + self.player.position.width / 2, self.player.position.y + self.player.position.height / 2)

			self.map.drawAll(self)
			self.player.sprites.draw(self.screen)

			pygame.display.flip()

	def text(self, txt, x, y):
		render = self.font.render(str(txt), 1, (0, 0, 0))
		self.screen.blit(render, (x, y))

	def leave(self):
		self.blnRunning = False
		pygame.quit()
