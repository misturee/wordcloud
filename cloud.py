#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont
import math, random

class TagCloud(object):

	# Need path to a font on the computer or add a font file to the directory
	FONT = '/Library/Fonts/WeibeiSC-Bold.otf'

	# Colors in the cloud
	FONT_COLOR = ['#F2B701', '#E57D04', '#DC0030', '#B10058', '#7C378A',
	 '#3465AA', '#09A275', '#85BC5F', '#39d', '#aab5f0']
	
	FONT_SIZE = [15, 17, 19, 21, 50]
				
	
	def __init__(self, width=800, height=800, radius=25):
		self.width = width
		self.height = height
		self.words_to_draw = None
		self.image = Image.new('RGBA', (width, height), "white")
		self.imageDraw = ImageDraw.Draw(self.image)
		self.spiral_radius = radius

	def draw(self, array, imgPath=None):
		self.array = array
		if imgPath is None:
			imgPath = self.get_rand_obj(array) + '.jpg'
		self.imgPath = imgPath
		
		first = self.array[0]
		last = self.array[-1]

		for i in range(len(self.array)):
			if i == len(self.array) - 1:
				weight = len(self.FONT_SIZE) - 1
			else:
				current = self.array[i]
				weight = self._rescaleWeight(current['weight'], first['weight'],
					last['weight'])
				self._findCoordinates(i, current['text'], int(weight))
		
		return self._save()
	
	def _rescaleWeight(self, n, max_weight, min_weight):
		try:
			weight = round((1.0 * (len(self.FONT_SIZE) - 1) *
			 	(n - min_weight)) / (max_weight - min_weight))
		except ZeroDivisionError:
			return len(self.FONT_SIZE) - 1

		return weight
	
	def _findCoordinates(self, index, text, weight):
		angleStep = 3.14 / 4
		radiusStep = 5
		angle = random.uniform(0.2, 6.28)

		font_size = self.FONT_SIZE[weight]
		width, height = self.imageDraw.textsize(text, 
			font=ImageFont.truetype(self.FONT, font_size))
		
		x = self.width/2
		y = self.height/2
		
		count = 1
		while self._checkOverlap(x, y, height, width):
			if count % 8 == 0:
				self.spiral_radius += radiusStep
			count += 1
			
			if index % 2 == 0:
				angle += angleStep
			else:
				angle += -angleStep
			
			x = self.width/2 + (self.spiral_radius*math.cos(angle))
			y = self.height/2 + self.spiral_radius*math.sin(angle)

		self.words_to_draw.append(
			{'text': text.decode('utf-8'), 'fontsize': font_size, 'x': x, 'y': y, 
			'w': width, 'h': height, 
			'color': self.FONT_COLOR[random.randint(0, len(self.FONT_COLOR) - 1)]})
		
	def _checkOverlap(self, x, y, h, w):
		if not self.words_to_draw:
			self.words_to_draw = []
			return False
		
		for word in self.words_to_draw:
			# Check for overlaps between array
			if not ((x+w < word['x']) or (word['x'] + word['w'] < x) or \
				(y + h < word['y']) or (word['y'] + word['h'] < y)):
				return True
		
		return False
	
	def _save(self):
		for word in self.words_to_draw:
			if self.inBoundary(word):
				self.imageDraw.text((word['x'], word['y']), word['text'], 
					font=ImageFont.truetype(self.FONT, word['fontsize']), 
					fill=word['color'])
			
		self.image.save(self.imgPath, "JPEG", quality=90)
		return self.imgPath

	def inBoundary(self, word):
		# Check if word lies within the image size
		return \
		word['x'] >= 0 and word['x'] + word['w'] <= self.width and \
		word['y'] >= 0 and word['y'] + word['h'] <= self.height
		
		
if __name__ == '__main__':

	t = TagCloud()

	def read_file(input_file):
		array = []
		output = open('chinese_Out', 'w')

		f = open(input_file, 'r')
		for line in f:
			lst = line.split()
			dct = {}
			dct['text'] = (lst[0])
			dct['weight'] = int(lst[1])
			array.append(dct)
		return array

	array = read_file('chineseRes3.txt')
	t.draw(array, 'cloud.jpg')
				