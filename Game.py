from __future__ import division
import math, sys, os, time, random, pickle
import pygame
from pygame import *

from Tank import Tank
from Objects import Food

class Game(object):

	NUM_OF_FOOD = 40
	NUM_OF_TANKS = 30
	NUM_OF_WINNERS = 5
	MUTATION_RATE = 0.15 # Out of 100
	ROUND_TIME = 40 # in seconds

	def __init__(self):
		self.window = pygame.display.set_mode((1280, 1024))
		self.surface = pygame.display.get_surface()
		self.entitylist = []

		self.clock = pygame.time.Clock()
		self.clock.tick(200)
		self.time = 0
		self.generation = 1
		self.abs_highscore = 0

		pygame.display.set_caption ("Evolution v1")

		try:
			text = open("data.evo", "r")
			best_brains = pickle.load(text)
			self.generation = best_brains.pop(0)
			text.close
		except:
			best_brains = []

		self.text_renderer = pygame.font.Font(None, 25)

		for i in range(self.NUM_OF_FOOD):
			self.createfood()

		for i in range(self.NUM_OF_TANKS):
			x = random.randint(0, self.surface.get_width())
			y = random.randint(0, self.surface.get_height())
			if len(best_brains) == 0:
				tank = Tank(self, x, y)
			else:
				tank = Tank(self, x, y, random.choice(best_brains))

	def createfood(self):
		x = random.randint(0, self.surface.get_width())
		y = random.randint(0, self.surface.get_height())
		food = Food(self, x, y)

	def restartmatch(self):
		highscores = self.get_highscores()

		for tank in highscores:
			highscores[highscores.index(tank)] = tank.brain.weights

		num_of_entities = len(self.entitylist)# Destroy everything
		for i in range(num_of_entities):
			entity = self.entitylist.pop(0)
			entity.destroy(self)

		print len(self.entitylist), num_of_entities

		for i in range(self.NUM_OF_TANKS):
			weightlist = []
			for weight in random.choice(highscores):# Take a brain from a random winner
				if random.random()*100 <= self.MUTATION_RATE:
					weight += 1-(random.random()*2)
				weightlist.append(weight)

			x = random.randint(0, self.surface.get_width())
			y = random.randint(0, self.surface.get_height())
			tank = Tank(self, x, y, weightlist)

		self.time = 0
		self.generation += 1

		text = open("data.evo", "w")
		pickle.dump([self.generation]+highscores, text)
		text.close()

	def run(self):
		for entity in self.entitylist:
			entity.step(self)

		self.draw()

		self.clock.tick(200)
		self.time += self.clock.get_time()
		if self.time > self.ROUND_TIME*1000:
			self.restartmatch()

	def get_highscores(self):
		highscores = []
		for entity in self.entitylist:
			if isinstance(entity, Tank):
				if len(highscores) < self.NUM_OF_WINNERS:# If the highscores aren't even filled, no point in comparing
					highscores.append(entity)
				else:
					for tank in highscores:
						if entity.score > tank.score:# If the new tank was more successfull then the old one
							highscores[highscores.index(tank)] = entity# Replace it
							break
		return highscores

	def draw(self):
		self.surface.fill((0, 0, 0))# Fill the screen with white
		for entity in self.entitylist:
			entity.draw(self)# self == game

		tmpscore = 0
		for highscore in self.get_highscores():
			tmpscore = max(tmpscore, highscore.score)

		self.abs_highscore = max(self.abs_highscore, tmpscore)

		rendered_text = self.text_renderer.render("Generation: "+str(self.generation)+"; Time left until change:"+str(round((self.ROUND_TIME*1000-self.time)/1000))+"; Highest Score this gen:"+str(tmpscore)+"; Absolute highest score:"+str(self.abs_highscore), 1, (0, 0, 255))
		textpos = rendered_text.get_rect(centerx=self.window.get_width()/2)
		self.surface.blit(rendered_text, textpos)

		pygame.display.flip()
