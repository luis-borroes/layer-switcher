import pygame

class Utils(object):

	def __init__(self):
		pass

	def approach(self, dt, num, target, step):
		if num > target:
			return max(num - step * dt * 100, target)

		elif num < target:
			return min(num + step * dt * 100, target)

		return num

	def collide(self, rect1, rect2):
		return not (rect1.left > rect2.right or rect1.right < rect2.left or rect1.top > rect2.bottom or rect1.bottom < rect2.top)

	def remap(self, v, min1, max1, min2, max2):
		return min2 + (v - min1) * (max2 - min2) / (max1 - min1)

	def boxText(self, text, width, font):
		words = text.split()
		line = ""
		lines = []
		lineCount = 0

		for word in words:
			size = font.size(line + word)

			if size[0] > width or word[0] == "\\":
				lines.append(line.strip())

				line = ""
				lineCount += 1

			line += (word if word[0] != "\\" else word[1:]) + " "

		lines.append(line.strip())
		lineCount += 1

		surface = pygame.Surface((width, (size[1] + 5) * lineCount), pygame.SRCALPHA | pygame.HWSURFACE)

		for i in xrange(lineCount):
			surface.blit(font.render(lines[i], 1, (0, 0, 0)), (surface.get_width() * 0.5 - font.size(lines[i])[0] * 0.5, (size[1] + 5) * i))

		return surface
