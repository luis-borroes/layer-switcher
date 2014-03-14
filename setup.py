from distutils.core import setup
import os, shutil, glob, fnmatch, py2exe, sys, json, hashlib

f = open("metadata", "w")
v = open("version.dat", "r")
metadata = {"version": v.readline().rstrip(), "files": {}}
v.close()

def hashfile(fn):
	hasher = hashlib.md5()
	buf = fn.read(8192)
	while len(buf) > 0:
		hasher.update(buf)
		buf = fn.read(8192)

	return hasher.hexdigest()

sys.argv.append("py2exe")
sys.path.append("./updater")

if os.path.isdir("layerswitcher"):
	shutil.rmtree("layerswitcher")

if os.path.isfile("layerswitcher.rar"):
	os.unlink("layerswitcher.rar")

origIsSystemDLL = py2exe.build_exe.isSystemDLL

def isSystemDLL(pathname):
	if os.path.basename(pathname).lower() in ("sdl_ttf.dll", "libfreetype-6.dll", "libogg-0.dll"):
		return False
	return origIsSystemDLL(pathname)
py2exe.build_exe.isSystemDLL = isSystemDLL

dist_dir = os.path.join("layerswitcher")
data_dir = dist_dir

class Game:
	name = "Layer Switcher"
	script = "main.pyw"
	dest_base = "layerswitcher"
	icon_resources = [(0, os.path.join("assets", "icons", "icon.ico"))]

class Updater:
	name = "Layer Switcher Updater"
	script = os.path.join("updater", "main.pyw")
	dest_base = "lwupdater"
	icon_resources = [(0, os.path.join("assets", "icons", "iconU.ico"))]

setup(
	options = {"py2exe": {"dist_dir": dist_dir, "optimize": 2, "bundle_files": 2, "compressed": 1, "dll_excludes": ["w9xpopen.exe"]}},
	zipfile = None,
	windows = [Game, Updater],
)

data = []
for dirpath, dirnames, filenames in os.walk("assets"):
	data.extend(os.path.join(dirpath, fn) for fn in filenames)

	metadata["files"][dirpath] = {}

	for fn in filenames:
		metadata["files"][dirpath][fn] = hashfile(open(os.path.join(dirpath, fn), "rb"))

for dirpath, dirnames, filenames in os.walk("maps"):
	data.extend(os.path.join(dirpath, fn) for fn in filenames)

	metadata["files"][dirpath] = {}

	for fn in filenames:
		metadata["files"][dirpath][fn] = hashfile(open(os.path.join(dirpath, fn), "rb"))

os.makedirs(data_dir + "/data")
data.extend(["version.dat"])
data.extend(["updater.dat"])

dest = data_dir
for fname in data:
	dname = os.path.join(dest, fname)
	if not os.path.exists(os.path.dirname(dname)):
		os.makedirs(os.path.dirname(dname))
	if not os.path.isdir(fname):
		shutil.copy(fname, dname)

json.dump(metadata, f, indent = 4)

f.close()

if os.path.isfile("c:\\dropbox\\public\\metadata"):
	os.unlink("c:\\dropbox\\public\\metadata")
shutil.move("metadata", "c:\\dropbox\\public")

if os.path.isdir("c:\\dropbox\\public\\layerswitcher"):
	shutil.rmtree("c:\\dropbox\\public\\layerswitcher")
shutil.copytree("layerswitcher", "c:\\dropbox\\public\\layerswitcher")

os.system("winrar a -r layerswitcher.rar layerswitcher")

if os.path.isfile("c:\\dropbox\\public\\layerswitcher.rar"):
	os.unlink("c:\\dropbox\\public\\layerswitcher.rar")
shutil.copy("layerswitcher.rar", "c:\\dropbox\\public")
