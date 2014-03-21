import pygame, button

class Options(object):

	def __init__(self, parent):
		self.parent = parent
		self.parent.currentMenu = "options"
		self.parent.menuObj = self

		button.Button.group = []

		button.Button("text", self.parent.mediumFont, "Set FPS:", (0, self.parent.resolution[1] - 385), self.parent.resolution)
		button.Button("small", self.parent.mediumFont, "30", (-125, self.parent.resolution[1] - 335), self.parent.resolution, lambda: self.setFPS(30))
		button.Button("small", self.parent.mediumFont, "60", (0, self.parent.resolution[1] - 335), self.parent.resolution, lambda: self.setFPS(60))
		button.Button("small", self.parent.mediumFont, "120", (125, self.parent.resolution[1] - 335), self.parent.resolution, lambda: self.setFPS(120))

		button.Button("text", self.parent.mediumFont, "Music volume:", (0, self.parent.resolution[1] - 275), self.parent.resolution)
		button.Button("small", self.parent.mediumFont, "-", (-75, self.parent.resolution[1] - 225), self.parent.resolution, self.lowerVolume)
		button.Button("small", self.parent.mediumFont, "+", (75, self.parent.resolution[1] - 225), self.parent.resolution, self.raiseVolume)

		button.Button("big", self.parent.mediumFont, "Back", (0, self.parent.resolution[1] - 150), self.parent.resolution, self.parent.mainMenu)

		button.Button("text", self.parent.mediumFont, "Set display:", (0, self.parent.resolution[1] - 495), self.parent.resolution)
		button.Button("big", self.parent.mediumFont, "Windowed" if self.parent.fullscreen else "Fullscreen", (0, self.parent.resolution[1] - 445), self.parent.resolution, self.toggleDisplay)

		for i in xrange(1, 4):
			if self.parent.fps == float(button.Button.group[i].rawText):
				button.Button.group[i].locked = True
			else:
				button.Button.group[i].locked = False

		if self.parent.volume == 0:
			button.Button.group[5].locked = True
		elif self.parent.volume == 20:
			button.Button.group[6].locked = True

	def setFPS(self, fps):
		self.parent.fps = fps
		for i in xrange(1, 4):
			if self.parent.fps == int(button.Button.group[i].rawText):
				button.Button.group[i].locked = True
			else:
				button.Button.group[i].locked = False

		self.parent.save.set("fps", fps)

	def lowerVolume(self):
		self.parent.volume = max(0, self.parent.volume - 1)
		if self.parent.volume == 0:
			button.Button.group[5].locked = True
		else:
			button.Button.group[5].locked = False
		button.Button.group[6].locked = False

		pygame.mixer.music.set_volume(self.parent.volume * 0.05)
		self.parent.save.set("volume", self.parent.volume)

	def raiseVolume(self):
		self.parent.volume = min(20, self.parent.volume + 1)
		if self.parent.volume == 20:
			button.Button.group[6].locked = True
		else:
			button.Button.group[6].locked = False
		button.Button.group[5].locked = False

		pygame.mixer.music.set_volume(self.parent.volume * 0.05)
		self.parent.save.set("volume", self.parent.volume)

	def toggleDisplay(self):
		self.parent.fullscreen = not self.parent.fullscreen
		button.Button.group[9].setText("Windowed" if self.parent.fullscreen else "Fullscreen")

		pygame.display.set_mode(self.parent.resolution, pygame.FULLSCREEN if self.parent.fullscreen else 0)
		self.parent.save.set("fullscreen", int(self.parent.fullscreen))
