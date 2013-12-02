#!/usr/bin/python

import pygame

import game

pygame.init()

class Main(object):
	def __init__(self):
		objClock = pygame.time.Clock()
		objScreen = pygame.display.set_mode((1280, 720))
		objGame = game.Game(pygame, objScreen, objClock)
		
Main()