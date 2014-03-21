#!/usr/bin/env python

import pygame, menu, os, sys, shutil, time

if os.path.isfile("lwupdater.exe.new"): #trigger updater rename
	time.sleep(2)
	try:
		shutil.move("lwupdater.exe.new", "lwupdater.exe")
	except:
		pass #usually it works even though it spits out an error, so lets supress that

if len(sys.argv) > 1 and sys.argv[1] == "-k": #used by the updater to trigger the rename but not run the game (when the updater is closed)
	sys.exit(0)

class Main(object):

	def __init__(self):
		version = "indev 0.1.0"

		with open("version.dat") as f:
			fVersion = f.readline().rstrip()

			if version != fVersion:
				version += " (f: %s)" % fVersion

		clock = pygame.time.Clock()
		fps = 120
		resolution = (1280, 720)

		icon = pygame.image.load("assets/icons/icon.png")
		pygame.display.set_icon(icon)
		pygame.display.set_caption("Layer Switcher", "Layer Switcher")

		screen = pygame.display.set_mode(resolution)

		pygame.mixer.music.load("assets/music/Pamgaea.mp3")
		pygame.mixer.music.set_volume(0.05)
		pygame.mixer.music.play(-1)

		objMenu = menu.Menu(screen, clock, fps, resolution, version)

if __name__ == "__main__":
	os.environ["SDL_VIDEO_CENTERED"] = "1"
	pygame.init()
	Main()
