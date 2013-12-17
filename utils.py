class Utils(object):

	def __init__(self):
		pass

	def approach(self, dt, num, target, step):
		if num > target:
			return max(num - step * dt * 100, target)
		elif num < target:
			return min(num + step * dt * 100, target)
		return num
