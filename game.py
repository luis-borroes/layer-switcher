class Game(object):
	pygame = False
	objScreen = False
	
	def __init__(self, pygame, objScreen, objClock):
		Game.pygame = pygame
		Game.objScreen = objScreen
		self.blnRunning = True

		sprites = pygame.sprites.Group()
		self.player = Player(pygame, sprites)

		while self.blnRunning:
			objClock.tick(30)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.leave()



	def leave(self):
		self.blnRunning = False
		Game.pygame.quit()