import pygame, subprocess, os, sys, shutil, button, urllib2, json, hashlib

class Updater(object):

	def __init__(self, screen, clock, fps, resolution, version):
		self.screen = screen
		self.clock = clock
		self.fps = fps
		self.resolution = resolution
		self.version = version
		self.latest = "searching..."

		self.small = pygame.font.Font("assets/ARLRDBD.ttf", 14)
		self.font = pygame.font.Font("assets/ARLRDBD.ttf", 30)

		self.running = True
		self.downloading = False

		button.Button("text", self.font, "Current version: %s" % self.version, (0, 10), self.resolution)
		button.Button("text", self.font, "Latest version: %s" % self.latest, (0, 45), self.resolution)
		button.Button("text", self.small, "", (0, 125), self.resolution)
		button.Button("big", self.font, "Update", (0, self.resolution[1] - 150), self.resolution, self.update)
		button.Button("big", self.font, "Play", (0, self.resolution[1] - 75), self.resolution, self.play)

		if self.version == self.latest:
			button.Button.group[3].locked = True

		while self.running:
			dt = self.clock.tick(self.fps)
			pygame.display.set_caption("Layer Switcher Updater", "Layer Switcher Updater")

			mouseTrigger = False

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.leave()

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.leave()

					if event.key == pygame.K_SPACE:
						self.play()

				if event.type == pygame.MOUSEBUTTONUP:
					if event.button == 1:
						mouseTrigger = True

			self.screen.fill((82, 246, 255))

			if self.downloading:
				self.downloadNext()

			mPos = pygame.mouse.get_pos()

			for butt in button.Button.group:
				butt.updateAndDraw(self.screen, mPos, mouseTrigger)

			pygame.display.flip()

			if self.latest == "searching...":
				self.getLink()
				self.checkUpdates()
				button.Button.group[1].setText("Latest version: %s" % self.latest)

	def getLink(self):
		self.link = ""
		with open("updater.dat") as f:
			self.link = f.readline().rstrip()

	def checkUpdates(self):
		self.latest = "n/a"

		buf = urllib2.urlopen(self.link + "metadata")
		self.metadata = json.load(buf)

		if len(self.metadata) > 0:
			self.latest = self.metadata["version"]

	def update(self):
		self.downloading = True
		self.toDownload = ["layerswitcher.exe", "version.dat", "updater.dat"]

		for folder in self.metadata["files"]:
			if not os.path.isdir(folder):
				os.makedirs(folder)

			for fn in self.metadata["files"][folder]:
				if not os.path.isfile(os.path.join(folder, fn)) or self.hashfile(open(os.path.join(folder, fn), "rb")) != self.metadata["files"][folder][fn]:
					self.toDownload.append(os.path.join(folder, fn))

		for dirpath, dirnames, filenames in os.walk("assets"):
			if not dirpath in self.metadata["files"]:
				shutil.rmtree(dirpath)
				continue

			for fn in filenames:
				if not fn in self.metadata["files"][dirpath]:
					os.unlink(os.path.join(dirpath, fn))

		for dirpath, dirnames, filenames in os.walk("maps"):
			if not dirpath in self.metadata["files"]:
				shutil.rmtree(dirpath)
				continue

			for fn in filenames:
				if not fn in self.metadata["files"][dirpath]:
					os.unlink(os.path.join(dirpath, fn))

		button.Button.group[2].setText(self.toDownload[-1])

	def downloadNext(self):
		if len(self.toDownload) > 0:
			fn = self.toDownload.pop()

			request = urllib2.urlopen(self.link + "layerswitcher/" + fn.replace("\\", "/").replace(" ", "%20"))

			with open(fn, "wb") as out:
				buf = request.read(8192)
				while len(buf) > 0:
					out.write(buf)
					buf = request.read(8192)
					
			if len(self.toDownload) > 0:
				button.Button.group[2].setText(self.toDownload[-1])

		else:
			self.downloading = False
			button.Button.group[0].setText("Current version: %s" % self.latest)
			button.Button.group[2].setText("Done!")
			button.Button.group[3].locked = True

	def play(self):
		subprocess.Popen("layerswitcher.exe")
		self.leave()

	def hashfile(self, fn):
		hasher = hashlib.md5()
		buf = fn.read(8192)
		while len(buf) > 0:
			hasher.update(buf)
			buf = fn.read(8192)

		return hasher.hexdigest()

	def leave(self):
		self.running = False
		pygame.quit()
		sys.exit(0)
