import pygame, subprocess, os, sys, shutil, button, urllib2, json, hashlib, threading

class Updater(object):

	def __init__(self, screen, clock, fps, resolution, version):
		self.screen = screen
		self.clock = clock
		self.fps = fps
		self.resolution = resolution
		self.version = version
		self.latest = "searching..."
		self.triggerSwap = False

		self.small = pygame.font.Font("assets/ARLRDBD.ttf", 14)
		self.font = pygame.font.Font("assets/ARLRDBD.ttf", 30)

		self.running = True
		self.downloading = False

		button.Button("text", self.font, "Current version: %s" % self.version, (0, 10), self.resolution)
		button.Button("text", self.font, "Latest version: %s" % self.latest, (0, 45), self.resolution)
		button.Button("text", self.small, "", (0, 125), self.resolution)
		button.Button("big", self.font, "Update", (0, self.resolution[1] - 150), self.resolution, self.update)
		button.Button("big", self.font, "Play", (0, self.resolution[1] - 75), self.resolution, self.play)

		button.Button.group[3].locked = True

		self.getLink()
		self.run(self.checkUpdates)

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

			mPos = pygame.mouse.get_pos()

			for butt in button.Button.group:
				butt.updateAndDraw(self.screen, mPos, mouseTrigger)

			pygame.display.flip()

	def getLink(self):
		self.link = ""
		with open("updater.dat") as f:
			self.link = f.readline().rstrip()

	def checkUpdates(self):
		try:
			buf = urllib2.urlopen(self.link + "metadata")
			self.metadata = json.load(buf)

			if len(self.metadata) > 0:
				self.latest = self.metadata["version"]

				if self.version == self.latest:
					button.Button.group[3].locked = True
				else:
					button.Button.group[3].locked = False

			button.Button.group[1].setText("Latest version: %s" % self.latest)

		except urllib2.HTTPError, e:
			button.Button.group[1].setText("Latest version: not found (%s)" % e.code)

	def update(self):
		button.Button.group[3].locked = True
		self.toDownload = ["version.dat", "updater.dat"]

		for folder in self.metadata["files"]:
			if folder != "layerswitcher":
				if not os.path.isdir(folder):
					os.makedirs(folder)

				for fn in self.metadata["files"][folder]:
					if not os.path.isfile(os.path.join(folder, fn)) or self.hashfile(open(os.path.join(folder, fn), "rb")) != self.metadata["files"][folder][fn]:
						self.toDownload.append(os.path.join(folder, fn))

			else:
				for fn in self.metadata["files"][folder]:
					if not os.path.isfile(fn) or self.hashfile(open(fn, "rb")) != self.metadata["files"][folder][fn]:
						self.toDownload.append(fn)

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

		self.run(self.downloadManager)

	def downloadManager(self):
		while len(self.toDownload) > 0:
			try:
				self.downloadNext()

			except urllib2.HTTPError, e:
				button.Button.group[2].setText("error - try again later")
				sys.exit(1)

		button.Button.group[0].setText("Current version: %s" % self.latest)
		button.Button.group[2].setText("Done!")

	def downloadNext(self):
		fn = self.toDownload.pop()
		button.Button.group[2].setText(fn)

		request = urllib2.urlopen(self.link + "layerswitcher/" + fn.replace("\\", "/").replace(" ", "%20"))
		total = int(request.info().getheader('Content-Length').strip())
		written = 0

		raw = fn
		if fn == "lwupdater.exe":
			fn += ".new"
			self.triggerSwap = True

		with open(fn, "wb") as out:
			buf = request.read(8192)

			while len(buf) > 0:
				out.write(buf)
				written += len(buf)
				button.Button.group[2].setText(raw + " - %d%%" % int((float(written) / total) * 100))

				buf = request.read(8192)

	def play(self):
		subprocess.Popen(["layerswitcher.exe"])
		self.leave()

	def run(self, call):
		t = threading.Thread(target = call)
		t.daemon = True
		t.start()

	def hashfile(self, fn):
		hasher = hashlib.md5()
		buf = fn.read(8192)
		while len(buf) > 0:
			hasher.update(buf)
			buf = fn.read(8192)

		return hasher.hexdigest()

	def leave(self):
		if self.triggerSwap:
			subprocess.Popen(["layerswitcher.exe", "-k"])

		self.running = False
		pygame.quit()
		sys.exit(0)
