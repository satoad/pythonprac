class Triangle:
	x1, x2, x3 = 0, 0, 0
	y1, y2, y3 = 0, 0, 0

	def __init__(self, *args):
		x1, x2, x3 = args[0][0], args[1][0], args[2][0]
		y1, y2, y3 = args[0][1], args[1][1], args[2][1]