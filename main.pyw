#!/usr/bin/env python

import pygame, menu, os

class Main(object):

	def __init__(self):
		version = "indev 0.0.1"

		clock = pygame.time.Clock()
		fps = 120.
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
