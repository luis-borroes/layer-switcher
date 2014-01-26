import pygame, player, enemy, mapper, viewport, animation, particles, item, sys, vector

class Game(object):

	def __init__(self, parent, world, mapname):
		self.running = True
		self.paused = False
		self.finished = False
		self.screen = parent.screen
		self.clock = parent.clock
		self.fps = parent.fps
		self.mediumFont = parent.mediumFont
		self.bigFont = parent.bigFont
		self.resolution = parent.resolution
		self.halfResolution = parent.halfResolution
		self.tileset = animation.Animation("assets/sprites/sheet.png", 70, 35, 1, 1)
		self.dt = 0
		self.returnValue = 0

		self.finishText = self.bigFont.render("Finished!", 1, (0, 0, 0))
		self.finishPos = vector.Vec2d(self.halfResolution[0] - self.finishText.get_width() // 2, -100)

		self.hintText = self.mediumFont.render("Press ESC to leave or SPACE to continue...", 1, (0, 0, 0))
		self.hintPos = vector.Vec2d(self.halfResolution[0] - self.hintText.get_width() // 2, self.resolution[1] + 150)

		self.map = mapper.Mapper(self, world, mapname)

		self.player = player.Player(self)
		self.viewport = viewport.Viewport(self, self.player.position.x, self.player.position.y)

		while self.running:
			self.dt = self.clock.tick(self.fps)
			pygame.display.set_caption("Layer Switcher %3d FPS" % (self.clock.get_fps()), "Layer Switcher")

			if self.dt > (1 / self.fps * 1000) + 20:
				self.dt = (1 / self.fps * 1000) + 20

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit(0)
					return

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						if self.paused:
							self.leave()
							return

						else:
							self.paused = True

					if event.key == pygame.K_w:
						self.player.key_w = True

					if event.key == pygame.K_s:
						self.player.key_s = True

					if event.key == pygame.K_SPACE:
						if self.finished:
							self.leave()
							self.returnValue = 1
							return

						elif self.paused:
							self.paused = False
						else:

							self.player.spaced = True

				if event.type == pygame.KEYUP:
					if event.key == pygame.K_SPACE:
						self.player.holdJump = False

			self.screen.fill(self.map.bgColor)
			self.map.drawBackground(self)

			if not self.paused:
				self.player.sprites.update(self, self.dt * 0.001)

				for gItem in item.Item.group:
					gItem.update(self, self.dt * 0.001)

				for gEnemy in enemy.Enemy.group:
					gEnemy.update(self, self.dt * 0.001)

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

					for gItem in item.Item.group:
						if realID == gItem.drawLayer:
							gItem.draw(self)

					for gEnemy in enemy.Enemy.group:
						if realID == gEnemy.drawLayer:
							gEnemy.draw(self)

					if realID == self.player.drawLayer:
						self.player.draw(self)

			endTrigger = True
			for keyHoles in self.map.keyHoles:
				if not keyHoles.done:
					endTrigger = False

			if endTrigger:
				self.paused = True
				self.finished = True

			if self.finished:
				if self.finishPos.y < 100:
					vec = vector.Vec2d(0, 100 - self.finishPos.y) * 0.005 * self.dt
					if vec.length < 0.05:
						vec = vector.Vec2d(0, 0)

					self.finishPos += vec

				if self.hintPos.y > self.resolution[1] - 100:
					vec = vector.Vec2d(0, self.resolution[1] - 100 - self.hintPos.y) * 0.005 * self.dt
					if vec.length < 0.05:
						vec = vector.Vec2d(0, 0)

					self.hintPos += vec

				self.screen.blit(self.finishText, self.finishPos)
				self.screen.blit(self.hintText, self.hintPos)

			pygame.display.flip()

	def text(self, txt, x = 0, y = 0):
		render = self.mediumFont.render(str(txt), 1, (0, 0, 0))
		self.screen.blit(render, (x, y))

	def leave(self):
		self.running = False
		particles.Particles.groups = []
		enemy.Enemy.group = []
		item.Item.group = []
