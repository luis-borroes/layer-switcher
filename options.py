import pygame, button

class Options(object):

	def __init__(self, parent):
		self.parent = parent
		self.parent.currentMenu = "options"

		button.Button.group = []

		button.Button("text", self.parent.mediumFont, "Set FPS:", (0, self.parent.resolution[1] - 385), self.parent.resolution, None)
		button.Button("small", self.parent.mediumFont, "30", (-125, self.parent.resolution[1] - 335), self.parent.resolution, lambda: self.setFPS(30.))
		button.Button("small", self.parent.mediumFont, "60", (0, self.parent.resolution[1] - 335), self.parent.resolution, lambda: self.setFPS(60.))
		button.Button("small", self.parent.mediumFont, "120", (125, self.parent.resolution[1] - 335), self.parent.resolution, lambda: self.setFPS(120.))

		button.Button("text", self.parent.mediumFont, "Music volume:", (0, self.parent.resolution[1] - 275), self.parent.resolution, None)
		button.Button("small", self.parent.mediumFont, "-", (-75, self.parent.resolution[1] - 225), self.parent.resolution, self.lowerVolume)
		button.Button("small", self.parent.mediumFont, "+", (75, self.parent.resolution[1] - 225), self.parent.resolution, self.raiseVolume)

		button.Button("big", self.parent.mediumFont, "Back", (0, self.parent.resolution[1] - 150), self.parent.resolution, self.parent.mainMenu)

	def setFPS(self, fps):
		self.parent.fps = fps

	def lowerVolume(self):
		self.parent.volume = max(0, self.parent.volume - 0.05)
		pygame.mixer.music.set_volume(self.parent.volume)

	def raiseVolume(self):
		self.parent.volume = min(1, self.parent.volume + 0.05)
		pygame.mixer.music.set_volume(self.parent.volume)
