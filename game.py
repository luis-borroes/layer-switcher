import pygame, player, mapper, viewport, animation, particles

class Game(object):

	def __init__(self, objScreen, objClock, fps, font, resolution):
		self.running = True
		self.paused = False
		self.screen = objScreen
		self.font = font
		self.resolution = resolution
		self.tileset = animation.Animation("assets/sprites/sheet.png", 70, 35, 1, 1)
		self.particleGroups = particles.Particles.groups

		self.map = mapper.Mapper(self, "World 1", "1 - Begin")

		self.player = player.Player(self)
		self.viewport = viewport.Viewport(self, self.player.position.x, self.player.position.y)

		while self.running:
			self.dt = objClock.tick(fps)
			pygame.display.set_caption("Layer Switcher %3d FPS" % (objClock.get_fps()), "Layer Switcher")

			if self.dt > (1 / fps * 1000) + 10:
				self.dt = (1 / fps * 1000) + 10

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.leave()
					return

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.leave()
						return

					if event.key == pygame.K_w:
						self.player.key_w = True

					if event.key == pygame.K_s:
						self.player.key_s = True

					if event.key == pygame.K_SPACE:
						self.player.spaced = True

			self.screen.fill(self.map.bgColor)
			self.map.drawBackground(self)

			if not self.paused:
				self.player.sprites.update(self, self.dt * 0.001)
				self.map.updateAll(self)
				self.particleGroups = particles.Particles.groups
				self.viewport.update(self, self.player.position.x + self.player.position.width / 2, self.player.position.y + self.player.position.height / 2)

			for layerID in xrange(self.map.layerCount):
				layer = self.map.totalLayers[layerID]
				layer.draw(self.screen)

				if layer in self.map.layers:
					realID = self.map.layers.index(layer)

					for group in self.particleGroups:
						group.draw(self, realID)

					if realID == self.player.drawLayer:
						self.player.draw(self)

			pygame.display.flip()

	def text(self, txt, x = 0, y = 0):
		render = self.font.render(str(txt), 1, (0, 0, 0))
		self.screen.blit(render, (x, y))

	def leave(self):
		self.running = False
		pygame.quit()
