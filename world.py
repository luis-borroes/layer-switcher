import pygame, game, button, os

class World(object):
	
	def __init__(self, parent):
		self.parent = parent
		self.parent.currentMenu = "world"

		self.worlds = os.listdir("maps") or [None]
		self.worldIndex = 0
		self.world = self.worlds[self.worldIndex]

		self.maps = os.listdir("maps/%s" % self.world) or [None]
		self.mapIndex = 0
		self.map = self.maps[self.mapIndex]

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

	def start(self):
		if self.world and self.map:
			self.parent.game = game.Game(self.parent, self.world, self.map)

			if self.parent.game.returnValue == 1:
				if self.mapIndex < len(self.maps) - 1:
					self.mapUp()
					self.start()

				elif self.worldIndex < len(self.worlds) - 1:
					self.worldUp()
					self.start()

				else:
					self.parent.mainMenu()

	def worldUp(self):
		if self.worldIndex < len(self.worlds) - 1:
			self.worldIndex += 1
			self.world = self.worlds[self.worldIndex]

			button.Button.group[4].setText(self.world)

			self.maps = os.listdir("maps/%s" % self.world) or [None]
			self.mapIndex = 0
			self.map = self.maps[self.mapIndex]

			button.Button.group[5].setText(self.map)

	def worldDown(self):
		if self.worldIndex > 0:
			self.worldIndex -= 1
			self.world = self.worlds[self.worldIndex]

			button.Button.group[4].setText(self.world)

			self.maps = os.listdir("maps/%s" % self.world) or [None]
			self.mapIndex = 0
			self.map = self.maps[self.mapIndex]

			button.Button.group[5].setText(self.map)

	def mapUp(self):
		if self.mapIndex < len(self.maps) - 1:
			self.mapIndex += 1
			self.map = self.maps[self.mapIndex]

			button.Button.group[5].setText(self.map)

	def mapDown(self):
		if self.mapIndex > 0:
			self.mapIndex -= 1
			self.map = self.maps[self.mapIndex]

			button.Button.group[5].setText(self.map)
