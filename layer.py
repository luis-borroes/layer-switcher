import pygame, block

class Layer(object):

	def __init__(self, parent, layer):
		self.parent = parent
		self.raw = layer

		self.blocks = {}

		if hasattr(self.raw, "decorations"):
			self.normal = False

			if layer.decorations == "":
				self.parent.drawable.append(self)

			else:
				self.parentID = int(layer.decorations)
				self.parent.layers[self.parentID].decor.append(self)

		else:
			self.normal = True
			self.decor = []
			self.grounds = []
			self.keyHoles = []

			self.normalID = len(self.parent.layers)

			self.parent.layers.append(self)
			self.parent.drawable.append(self)

		for x in xrange(0, self.parent.tilemap.width):

			if self.normal:
				self.grounds.append([])
				nextGround = True

			for y in xrange(0, self.parent.tilemap.height):
				img = self.parent.tilemap.getTileImage(x, y, self.parent.layerCount)
				
				if img:
					rawBlock = block.Block(x, y, self.parent.tilemap, img, self.parent.layerCount)
					self.blocks[(x, y)] = rawBlock

					if self.normal:
						if "keyhole" in rawBlock.prop:
							self.keyHoles.append(rawBlock)
							self.parent.hasKeyHoles = True

							if (x, y - 1) in self.blocks and "keyhole" in self.blocks[(x, y - 1)].prop:
								self.keyHoles.remove(self.blocks[(x, y - 1)])

						if nextGround and (rawBlock.collidable and not "c" in rawBlock.prop) or (rawBlock.liquid and not self.blocks[(x, y - 1)].liquid):
							self.grounds[-1].append(rawBlock)

							if rawBlock.liquid:
								nextGround = True
							else:
								nextGround = False

				elif self.normal:
					nextGround = True

	def draw(self, game):
		for x in xrange(game.viewport.rect.left / self.parent.tilemap.tilewidth, game.viewport.rect.right / self.parent.tilemap.tilewidth + 1):
			for y in xrange(game.viewport.rect.top / self.parent.tilemap.tileheight, game.viewport.rect.bottom / self.parent.tilemap.tileheight + 1):
				if (x, y) in self.blocks:
					rawBlock = self.blocks[(x, y)]
					game.screen.blit(rawBlock.image, (rawBlock.position.x - game.viewport.rect.x, rawBlock.position.y - game.viewport.rect.y))
