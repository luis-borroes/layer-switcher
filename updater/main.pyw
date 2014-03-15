#!/usr/bin/env python

import pygame, os, shutil, sys, updater

if os.path.basename(sys.argv[0]) == "main.pyw": #running from source, chdir up (__file__ isn't defined in the compiled version)
	os.chdir("..")

class Main(object):

	def __init__(self):
		version = ""

		with open("version.dat") as f:
			version = f.readline().rstrip()

		clock = pygame.time.Clock()
		fps = 60
		resolution = (720, 360)

		icon = pygame.image.load("assets/icons/iconU.png")
		pygame.display.set_icon(icon)
		pygame.display.set_caption("Layer Switcher Updater", "Layer Switcher Updater")

		screen = pygame.display.set_mode(resolution)

		objUploader = updater.Updater(screen, clock, fps, resolution, version)

if __name__ == "__main__":
	os.environ["SDL_VIDEO_CENTERED"] = "1"
	pygame.init()
	Main()
