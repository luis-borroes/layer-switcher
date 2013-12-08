#!/usr/bin/python

import pygame, game

class Main(object):
	def __init__(self):
		objClock = pygame.time.Clock()
		objScreen = pygame.display.set_mode((1280, 720))
		objGame = game.Game(objScreen, objClock)

if __name__ == "__main__":
	pygame.init()
	Main()