import pygame, game, button, os, save

class World(object):
	
	def __init__(self, parent):
		self.parent = parent
		self.parent.currentMenu = "world"

		self.save = save.Save("save")
		self.data = self.save.load()

		self.genWorlds()

		self.world = self.unlockedWorlds[-1]
		self.worldIndex = self.worlds.index(self.world) if self.world and self.worlds.count(self.world) > 0 else 0
		self.world = self.worlds[self.worldIndex]

		self.genMaps()

		self.map = self.unlockedMaps[-1]
		self.mapIndex = self.maps.index(self.map[self.map.find(":") + 1:]) if self.map and self.maps.count(self.map[self.map.find(":") + 1:]) > 0 else 0
		self.map = self.maps[self.mapIndex]

		self.locked = not (self.world and self.map)

		parent.world = self

		button.Button.group = []

		button.Button("small", self.parent.mediumFont, "<", (-205, self.parent.resolution[1] - 450), self.parent.resolution, self.worldDown)
		button.Button("small", self.parent.mediumFont, ">", (205, self.parent.resolution[1] - 450), self.parent.resolution, self.worldUp)
		button.Button("small", self.parent.mediumFont, "<", (-205, self.parent.resolution[1] - 325), self.parent.resolution, self.mapDown)
		button.Button("small", self.parent.mediumFont, ">", (205, self.parent.resolution[1] - 325), self.parent.resolution, self.mapUp)

		button.Button("medium", self.parent.mediumFont, self.world, (0, self.parent.resolution[1] - 475), self.parent.resolution, None)
		button.Button("medium", self.parent.mediumFont, self.map, (0, self.parent.resolution[1] - 350), self.parent.resolution, None)

		button.Button("big", self.parent.mediumFont, "Start", (0, self.parent.resolution[1] - 225), self.parent.resolution, self.start)
		button.Button("big", self.parent.mediumFont, "Back", (0, self.parent.resolution[1] - 150), self.parent.resolution, self.parent.mainMenu)

		if self.worldIndex == 0:
			button.Button.group[0].locked = True
		if self.worldIndex == len(self.worlds) - 1:
			button.Button.group[1].locked = True

		if self.mapIndex == 0:
			button.Button.group[2].locked = True
		if self.mapIndex == len(self.maps) - 1:
			button.Button.group[3].locked = True

	def start(self):
		if self.world and self.map and not self.locked:
			if self.mapIndex == len(self.maps) - 1:
				spec = True
			else:
				spec = False

			self.parent.game = game.Game(self.parent, self.world, self.map, spec)

			if self.parent.game.returnValue != 0:
				self.data = self.save.load()
				self.genWorlds(False)
				self.genMaps(False)

			if self.parent.game.returnValue in (1, 3):
				if self.mapIndex < len(self.maps) - 1:
					self.mapUp()
					if self.parent.game.returnValue == 1:
						self.start()

			elif self.parent.game.returnValue in (2, 4):
				if self.worldIndex < len(self.worlds) - 1:
					self.worldUp()
					if self.parent.game.returnValue == 2:
						self.start()

				else:
					self.parent.mainMenu()

	def worldUp(self):
		if self.worldIndex < len(self.worlds) - 1:
			self.worldIndex += 1
			self.world = self.worlds[self.worldIndex]

			if self.worldIndex == len(self.worlds) - 1:
				button.Button.group[1].locked = True

			button.Button.group[0].locked = False

			button.Button.group[4].setText(self.world)

			self.genMaps()

			button.Button.group[5].setText(self.map)

			if not self.world in self.unlockedWorlds:
				button.Button.group[4].locked = True
				button.Button.group[5].locked = True
				button.Button.group[6].locked = True
				self.locked = True
			else:
				button.Button.group[4].locked = False
				button.Button.group[5].locked = False
				button.Button.group[6].locked = False
				self.locked = False

			button.Button.group[2].locked = True
			button.Button.group[3].locked = False

	def worldDown(self):
		if self.worldIndex > 0:
			self.worldIndex -= 1
			self.world = self.worlds[self.worldIndex]

			if self.worldIndex == 0:
				button.Button.group[0].locked = True

			button.Button.group[1].locked = False

			button.Button.group[4].setText(self.world)

			self.genMaps()

			button.Button.group[5].setText(self.map)

			if self.worldIndex > 0 and not self.world in self.unlockedWorlds:
				button.Button.group[4].locked = True
				button.Button.group[5].locked = True
				button.Button.group[6].locked = True
				self.locked = True
			else:
				button.Button.group[4].locked = False
				button.Button.group[5].locked = False
				button.Button.group[6].locked = False
				self.locked = False

			button.Button.group[2].locked = True
			button.Button.group[3].locked = False

	def mapUp(self):
		if self.mapIndex < len(self.maps) - 1:
			self.mapIndex += 1
			self.map = self.maps[self.mapIndex]

			if self.mapIndex == len(self.maps) - 1:
				button.Button.group[3].locked = True

			button.Button.group[2].locked = False

			button.Button.group[5].setText(self.map)

			if not self.world + ":" + self.map in self.unlockedMaps:
				button.Button.group[5].locked = True
				button.Button.group[6].locked = True
				self.locked = True
			else:
				button.Button.group[5].locked = False
				button.Button.group[6].locked = False
				self.locked = False

	def mapDown(self):
		if self.mapIndex > 0:
			self.mapIndex -= 1
			self.map = self.maps[self.mapIndex]

			if self.mapIndex == 0:
				button.Button.group[2].locked = True

			button.Button.group[3].locked = False

			button.Button.group[5].setText(self.map)

			if (self.worldIndex > 0 or self.mapIndex > 0) and not self.world + ":" + self.map in self.unlockedMaps:
				button.Button.group[5].locked = True
				button.Button.group[6].locked = True
				self.locked = True
			else:
				button.Button.group[5].locked = False
				button.Button.group[6].locked = False
				self.locked = False

	def genWorlds(self, index = True):
		self.worlds = os.listdir("maps") or [None]
		self.unlockedWorlds = []

		previous = None
		for i in self.worlds:
			if previous in self.data:
				self.unlockedWorlds.append(i)

			previous = i

		if len(self.unlockedWorlds) == 0:
			self.unlockedWorlds = [None]

		if index:
			self.worldIndex = 0
			self.world = self.worlds[self.worldIndex]

	def genMaps(self, index = True):
		self.maps = os.listdir("maps/%s" % self.world) or [None]
		self.unlockedMaps = []

		previous = None
		for i in self.maps:
			if previous in self.data:
				self.unlockedMaps.append(self.world + ":" + i)

			previous = self.world + ":" + i

		if len(self.unlockedMaps) == 0:
			self.unlockedMaps = [None]

		if index:
			self.mapIndex = 0
			self.map = self.maps[self.mapIndex]
