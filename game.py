import pygame, player, enemy, mapper, viewport, animation, particles, sys

class Game(object):

	def __init__(self, screen, clock, fps, font, resolution, halfResolution):
		self.running = True
		self.paused = False
		self.screen = screen
		self.clock = clock
		self.fps = fps
		self.font = font
		self.resolution = resolution
		self.halfResolution = halfResolution
		self.tileset = animation.Animation("assets/sprites/sheet.png", 70, 35, 1, 1)

		self.map = mapper.Mapper(self, "World 1", "1 - Begin")

		self.player = player.Player(self)
		self.viewport = viewport.Viewport(self, self.player.position.x, self.player.position.y)

		while self.running:
			self.dt = self.clock.tick(self.fps)
			pygame.display.set_caption("Layer Switcher %3d FPS" % (self.clock.get_fps()), "Layer Switcher")

			if self.dt > (1 / self.fps * 1000) + 10:
				self.dt = (1 / self.fps * 1000) + 10

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit(0)
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

				for gEnemy in enemy.Enemy.group:
					gEnemy.update(self, self.dt * 0.001)

				self.map.updateAll(self)
				self.viewport.update(self, self.player.position.centerx, self.player.position.centery)

			for layerID in xrange(self.map.layerCount + 1):
				layer = self.map.totalLayers[layerID]

				if not layer in self.map.specialDecos:
					layer.draw(self.screen)

				if layer in self.map.layers:
					realID = self.map.layers.index(layer)

					if realID in self.map.decoLinks:
						for subLayer in self.map.decoLinks[realID]:
							subLayer.draw(self.screen)

					for group in particles.Particles.groups:
						group.draw(self, realID)

					for gEnemy in enemy.Enemy.group:
						if realID == gEnemy.drawLayer:
							gEnemy.draw(self)

					if realID == self.player.drawLayer:
						self.player.draw(self)

			pygame.display.flip()

	def text(self, txt, x = 0, y = 0):
		render = self.font.render(str(txt), 1, (0, 0, 0))
		self.screen.blit(render, (x, y))

	def leave(self):
		self.running = False
		particles.Particles.groups = []
		enemy.Enemy.group = []
