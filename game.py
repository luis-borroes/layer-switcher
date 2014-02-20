import pygame, player, enemy, mapper, viewport, animation, particles, item, sys, vector, save, utils, timer
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

		self.finishText = self.bigFont.render("Finished!", 1, (0, 0, 0))
		self.finishPos = vector.Vec2d(self.halfResolution[0] - self.finishText.get_width() * 0.5, -100)

		self.hintText = self.mediumFont.render("Press ESC to leave or SPACE to continue...", 1, (0, 0, 0))
		self.hintPos = vector.Vec2d(self.halfResolution[0] - self.hintText.get_width() * 0.5, self.resolution[1] + 150)

		self.recordText = self.mediumFont.render("New record!", 1, (0, 0, 0))
		self.recordPos = vector.Vec2d(-100, self.halfResolution[1] - 80)

		self.timeText = None
		self.timePos = vector.Vec2d(self.resolution[0] + 100, self.halfResolution[1] - 20)

		self.bestText = None
		self.bestPos = vector.Vec2d(-100, self.halfResolution[1] + 20)

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

			if not self.paused:
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
					self.timeText = self.mediumFont.render("time: " + self.timer.text + "!", 1, (0, 0, 0))
					self.bestText = self.mediumFont.render("best: " + self.timer.text + "!", 1, (0, 0, 0))
				else:
					self.timeText = self.mediumFont.render("time: " + self.timer.text, 1, (0, 0, 0))
					self.bestText = self.mediumFont.render("best: " + self.timer.textBest, 1, (0, 0, 0))


			if self.finished:
				self.drawFinished()

			self.timer.updateAndDraw(self)

			pygame.display.flip()

	def text(self, txt, x = 0, y = 0):
		render = self.mediumFont.render(str(txt), 1, (0, 0, 0))
		self.screen.blit(render, (x, y))

	def drawFinished(self):
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

		if self.timePos.x > self.halfResolution[0] - 100 - self.timeText.get_width() * 0.5:
			vec = vector.Vec2d(self.halfResolution[0] - 100 - self.timeText.get_width() * 0.5 - self.timePos.x, 0) * 0.005 * self.dt
			if vec.length < 0.05:
				vec = vector.Vec2d(0, 0)

			self.timePos += vec

		if self.bestPos.x < self.halfResolution[0] + 100 - self.bestText.get_width() * 0.5:
			vec = vector.Vec2d(self.halfResolution[0] + 100 - self.bestText.get_width() * 0.5 - self.bestPos.x, 0) * 0.005 * self.dt
			if vec.length < 0.05:
				vec = vector.Vec2d(0, 0)

			self.bestPos += vec

		self.screen.blit(self.finishText, self.finishPos)
		self.screen.blit(self.hintText, self.hintPos)
		self.screen.blit(self.timeText, self.timePos)
		self.screen.blit(self.bestText, self.bestPos)

		if self.timer.best == "n/a" or self.timer.current < self.timer.best:
			if self.recordPos.x < self.halfResolution[0] - self.recordText.get_width() * 0.5:
				vec = vector.Vec2d(self.halfResolution[0] - self.recordText.get_width() * 0.5 - self.recordPos.x, 0) * 0.005 * self.dt
				if vec.length < 0.05:
					vec = vector.Vec2d(0, 0)

				self.recordPos += vec

			self.screen.blit(self.recordText, self.recordPos)

	def leave(self):
		self.running = False
		particles.Particles.groups = []
		enemy.Enemy.group = []
		item.Item.group = []
