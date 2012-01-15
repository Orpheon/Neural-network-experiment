from __future__ import division
import math, sys, os, time, random
import pygame
from pygame import *

from Objects import GameObject, Food
from NeuralNet import NeuralNet

class Tank(GameObject):

	maxspeed = 5
	maxturnspeed = 0.3
	size = 15
	color = (255, 0, 0)# Red

	def __init__(self, game, x, y, brain_weights=[]):
		GameObject.__init__(self, game, x, y)
		self.speed = 0
		self.direction = 90
		self.score = 0
		self.brain = NeuralNet(brain_weights)


	def get_nearest_food(self, game):

		# Find the nearest food instance
		nearestfood = -1
		for food in game.entitylist:
			if isinstance(food, Food):# If the entity is a food entity
				if nearestfood == -1:
					nearestfood = food
					distance = math.hypot(self.x-food.x, self.y-food.y)
				elif math.hypot(self.x-food.x, self.y-food.y) < distance:
					nearestfood = food
					distance = math.hypot(self.x-food.x, self.y-food.y)

		return nearestfood


	def step(self, game):

		nearestfood = self.get_nearest_food(game)

		# Get the values needed by the brain
		looking_at = (math.cos(self.direction), math.sin(self.direction))# Where am I looking at?

		nearestfood_vector_length = math.hypot(nearestfood.x-self.x, nearestfood.y-self.y)
		nearestfood_vector = ((nearestfood.x-self.x)/nearestfood_vector_length, (nearestfood.y-self.y)/nearestfood_vector_length)# In what direction is the nearest food?

		# Run the brain
		motorleft, motorright = self.brain.run((looking_at, nearestfood_vector))

		# Turn the tank
		rotation = motorleft-motorright # Get the direction changes
		rotation = min(self.maxturnspeed, max(self.maxturnspeed*(-1), rotation)) # Clamp to the max rotation
		self.direction = (self.direction+rotation) % 360 # Add the rotation to the self.direction

		# Update the speed
		self.speed = min(self.maxspeed, max(self.maxspeed*(-1), motorleft + motorright))

		# Check collision with the nearest food.
		if math.hypot(self.x-nearestfood.x, self.y-nearestfood.y) < self.size:
			self.score += 1
			nearestfood.destroy(game)

		# Move the tanks according to the speed
		self.x += math.cos(self.direction)*self.speed
		self.y += math.sin(self.direction)*self.speed

		# Make the borders of the game go in one-another
		if self.x < 0:# Exceeded left border
			self.x = game.surface.get_width()-self.x
		elif self.x > game.surface.get_width():# Exceeded right border
			self.x = self.x-game.surface.get_width()

		if self.y < 0:# Exceeded top border
			self.y = game.surface.get_height()-self.y
		elif self.y > game.surface.get_height():# Exceeded bottom border
			self.y = self.y-game.surface.get_height()


	def draw(self, game):
		rect = pygame.Rect(0, 0, self.size, self.size)
		rect.center = (self.x, self.y)
		if self in game.get_highscores():
			color = (255, 255, 0)# Yellow
		else:
			color = self.color# Red

		pygame.draw.rect(game.surface, color, rect)
		pygame.draw.line(game.surface, color, (self.x, self.y), (self.x+math.cos(self.direction)*(self.size+10), self.y+math.sin(self.direction)*(self.size+10)))


	def destroy(self, game):
		self.brain = 0
		GameObject.destroy(self, game)
