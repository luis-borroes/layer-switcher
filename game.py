import pygame, player, enemy, mapper, viewport, animation, particles, item, sys, button, save, utils, timer
util = utils.Utils()

class Game(object):

	def __init__(self, parent, world, mapName, spec):
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
		self.world = world
		self.mapName = mapName

		self.save = save.Save("save")
		self.data = self.save.load()

		self.movingTexts = [
			button.MovingText("Finished!", self.bigFont, (self.halfResolution[0], -100), (self.halfResolution[0], 100)),
			button.MovingText("Press ESC to leave or SPACE to continue", self.mediumFont, (self.halfResolution[0], self.resolution[1] + 150), (self.halfResolution[0], self.resolution[1] - 100)),
			button.MovingText("n/a", self.mediumFont, (self.resolution[0] + 150, self.halfResolution[1] - 20), (self.halfResolution[0] - 100, self.halfResolution[1] - 20)),
			button.MovingText("n/a", self.mediumFont, (-150, self.halfResolution[1] + 20), (self.halfResolution[0] + 100, self.halfResolution[1] + 20)),
			button.MovingText("New record!", self.mediumFont, (-150, self.halfResolution[1] - 90), (self.halfResolution[0], self.halfResolution[1] - 90))
		]

		self.timer = timer.Timer(self)

		self.map = mapper.Mapper(self, self.world, self.mapName)

		self.player = player.Player(self)
		self.viewport = viewport.Viewport(self, self.player.position.x, self.player.position.y)

		while self.running:
			self.dt = self.clock.tick(self.fps)
			pygame.display.set_caption("Layer Switcher %3d FPS" % (self.clock.get_fps()), "Layer Switcher")

			if self.dt > 120:
				self.dt = 120

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit(0)
					return

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						if self.paused:
							self.leave()
							if self.finished:
								if spec:
									self.returnValue = 4
								else:
									self.returnValue = 3

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
							if spec:
								self.returnValue = 2
							else:
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

			if not self.paused and not self.player.isDead:
				self.player.update(self, self.dt * 0.001)

				for gItem in item.Item.group:
					gItem.update(self, self.dt * 0.001)

				for gEnemy in enemy.Enemy.group:
					gEnemy.update(self, self.dt * 0.001)
					if util.collide(self.player.position, gEnemy.position) and self.player.layer == gEnemy.layer:
						self.player.die(self)

				self.viewport.update(self, self.player.position.centerx, self.player.position.centery)

			endTrigger = True

			for layer in self.map.drawable:
				layer.draw(self)

				if layer.normal:
					for subLayer in layer.decor:
						subLayer.draw(self)

					for group in particles.Particles.groups:
						group.draw(self, layer.normalID)

					for gItem in item.Item.group:
						if layer.normalID == gItem.drawLayer:
							gItem.draw(self)

					for gEnemy in enemy.Enemy.group:
						if layer.normalID == gEnemy.drawLayer:
							gEnemy.draw(self)

					if layer.normalID == self.player.drawLayer:
						self.player.draw(self)

					for keyHole in layer.keyHoles:
						if not keyHole.done:
							endTrigger = False

			if endTrigger and self.map.hasKeyHoles and not self.finished:
				self.paused = True
				self.finished = True

				if spec:
					self.data[self.map.world] = "1"

				if self.map.world + ":" + self.map.mapName in self.data:
					if self.timer.current < float(self.data[self.map.world + ":" + self.map.mapName]):
						self.data[self.map.world + ":" + self.map.mapName] = self.timer.current

				else:
					self.data[self.map.world + ":" + self.map.mapName] = self.timer.current

				self.save.save(self.data)

				if self.timer.best == "n/a" or self.timer.current < self.timer.best:
					self.movingTexts[2].setText("time: %s!" % self.timer.text)
					self.movingTexts[3].setText("best: %s!" % self.timer.text)
				else:
					self.movingTexts[2].setText("time: %s" % self.timer.text)
					self.movingTexts[3].setText("best: %s" % self.timer.textBest)

			if self.finished:
				self.drawFinished()

			self.timer.updateAndDraw(self)

			pygame.display.flip()

	def text(self, txt, x = 0, y = 0):
		render = self.mediumFont.render(str(txt), 1, (0, 0, 0))
		self.screen.blit(render, (x, y))

	def drawFinished(self):
		for mov in xrange(len(self.movingTexts)):
			if mov != 4 or (self.timer.best == "n/a" or self.timer.current < self.timer.best):
				self.movingTexts[mov].updateAndDraw(self)

	def leave(self):
		self.running = False
		particles.Particles.groups = []
		enemy.Enemy.group = []
		item.Item.group = []
