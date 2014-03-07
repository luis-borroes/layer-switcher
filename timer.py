import pygame

class Timer(object):

	def __init__(self, game):
		self.current = 0.

		worldData = game.save.get(game.world)

		if worldData and game.mapName in worldData:
			self.best = float(worldData[game.mapName])
			m, s = divmod(self.best, 60.)
			self.textBest = str(int(m)) + ":%2.3f" % s
			self.renderedBest = game.mediumFont.render(self.textBest, 1, (0, 0, 0))

		else:
			self.best = "n/a"
			self.textBest = "n/a"
			self.renderedBest = game.mediumFont.render(self.textBest, 1, (0, 0, 0))

		self.render(game)

	def updateAndDraw(self, game):
		if not game.finished:
			self.current += game.dt * 0.001
			self.render(game)

		game.screen.blit(self.rendered, (10, 5))
		game.screen.blit(self.renderedBest, (10, 45))

	def render(self, game):
		m, s = divmod(self.current, 60.)
		self.text = str(int(m)) + ":%2.3f" % s
		self.rendered = game.mediumFont.render(self.text, 1, (0, 0, 0))

	def reset(self, game):
		self.current = 0.
		self.real = 0
		self.render(game)
