from __future__ import division
import math, sys, os, time, random
import pygame
from pygame.locals import *

class GameObject(object):
	def __init__(self, game, x, y):
		self.x, self.y = x, y
		game.entitylist.append(self)

	def step(self, game): pass

	def draw(self, game):
		pass

	def destroy(self, game):
		if self in game.entitylist:
			# Remove the object from the object lists
			game.entitylist.remove(self)


class Food(GameObject):

	size = 10
	color = (0, 255, 0)# Green

	def draw(self, game):
		pygame.draw.circle(game.surface, self.color, (self.x, self.y), self.size)

	def destroy(self, game):
		GameObject.destroy(self, game)
		game.createfood()
