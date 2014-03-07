import pygame, json, os

class Save(object):

	def __init__(self, saveType):
		if saveType == "opt":
			self.filename = "data/config.dat"
		elif saveType == "save":
			self.filename = "data/save.dat"

		if not os.path.isfile(self.filename) or os.path.getsize(self.filename) == 0:
			with open(self.filename, "w+") as f:
				json.dump({"volume": 1, "fps": 120, "fullscreen": 0, "displayTip": 1} if saveType == "opt" else {}, f)
				f.close()

		self.data = {}
		self.load()

	def save(self):
		with open(self.filename, "w+") as f:
			json.dump(self.data, f)
			f.close()

	def load(self):
		with open(self.filename, "r") as f:
			self.data = json.load(f)
			f.close()

	def set(self, key, value):
		self.data[key] = value
		self.save()

	def add(self, key, value):
		if key in self.data:
			self.data[key].update(value)
		else:
			self.set(key, value)

		self.save()

	def get(self, key):
		if key in self.data:
			return self.data[key]

		return None
