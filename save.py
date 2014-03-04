import pygame, json, os

class Save(object):

	def __init__(self, saveType):
		if saveType == "opt":
			self.filename = "data/config.dat"
		elif saveType == "save":
			self.filename = "data/save.dat"

		if not os.path.isfile(self.filename) or os.path.getsize(self.filename) == 0:
			with open(self.filename, "w+") as f:
				json.dump({"volume": 0.05, "fps": 120., "fullscreen": 0, "displayTip": 1} if saveType == "opt" else {}, f)
				f.close()

	def save(self, arr):
		with open(self.filename, "w+") as f:
			json.dump(arr, f)
			f.close()

	def load(self):
		data = {}

		with open(self.filename, "r") as f:
			data = json.load(f)
			f.close()

		return data
