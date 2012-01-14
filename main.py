from __future__ import division
import math, sys, os, time, random
import pygame
from pygame import *

from Game import Game
from Tank import Tank
from Objects import Food

pygame.init()

game = Game()
while True:
	game.run()
