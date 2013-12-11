#!/usr/bin/python

import pygame, game

class Main(object):
	def __init__(self):
		objClock = pygame.time.Clock()
		fps = 120.
		icon = pygame.image.load("assets/icon32fix.png")
		pygame.display.set_icon(icon)
		pygame.display.set_caption("pyg", "pyg")
		objScreen = pygame.display.set_mode((1280, 720))
		objGame = game.Game(objScreen, objClock, fps)

if __name__ == "__main__":
	pygame.init()
	Main()
