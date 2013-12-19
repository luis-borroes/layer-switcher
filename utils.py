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
		if rect1.left > rect2.right:
			return False

		if rect1.right < rect2.left:
			return False

		if rect1.top > rect2.bottom:
			return False

		if rect1.bottom < rect2.top:
			return False

		return True
