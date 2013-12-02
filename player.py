class Player(pygame.sprite.Sprite):
	pygame = False

	def __init__(self, pygame, *groups):
		Player.pygame = pygame
		super(Player, self).__init__(*groups)

		self.image = pygame.image.load('tiles/player.png')
		self.rect = pygame.rect.Rect((320, 240), self.image.get_size())

	def move(self):
		pygame = Player.pygame
		keys = pygame.key.get_pressed()

		if key[pygame.KEY_LEFT]:
			self.rect.x -= 10
		if key[pygame.KEY_RIGHT]:
			self.rect.x += 10
		if key[pygame.KEY_UP]:
			self.rect.y += 10
		if key[pygame.KEY_DOWN]:
			self.rect.y -= 10