#!/usr/bin/env python

import pygame, menu

class Main(object):

	def __init__(self):
		clock = pygame.time.Clock()
		fps = 120.
		resolution = (1280, 720)

		icon = pygame.image.load("assets/icons/icon.png")
		pygame.display.set_icon(icon)
		pygame.display.set_caption("Layer Switcher", "Layer Switcher")

		screen = pygame.display.set_mode(resolution)
		font = pygame.font.Font("assets/ARLRDBD.ttf", 30)

		objMenu = menu.Menu(screen, clock, fps, font, resolution)

if __name__ == "__main__":
	pygame.init()
	Main()
