import pygame

from vector import Vec2d as Vector

class Block(object):

	def __init__(self, x, y, objMap, img, layer):
		self.image = img
		self.tilex = x
		self.tiley = y

		self.x = x * objMap.tilewidth
		self.y = y * objMap.tileheight

		self.position = pygame.rect.Rect((self.x, self.y), self.image.get_size())

		self.prop = objMap.getTileProperties((x, y, layer)) or {}
		self.collidable = "l" in self.prop or "r" in self.prop or "u" in self.prop or "d" in self.prop or "c" in self.prop
		self.liquid = "w" in self.prop or "m" in self.prop
		self.hooked = False
		self.done = False
		self.slope = False

		if "o" in self.prop and self.prop["o"] != "":
			key = (0, 255, 255)
			surf = pygame.Surface(self.image.get_size())
			surf.fill(key)
			surf.set_colorkey(key)
			surf.blit(self.image, (0, 0))
			surf.set_alpha(int(self.prop["o"]), pygame.RLEACCEL)

			self.image = surf.convert_alpha()

		if "i" in self.prop:
			self.image = pygame.Surface(self.image.get_size(), pygame.SRCALPHA | pygame.HWSURFACE)

		if "p" in self.prop:
			self.slope = self.prop["p"]
