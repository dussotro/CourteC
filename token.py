class Token:

	def __init__(self, kind, value, position):
		self.kind = kind
		self.value = value
		self.position = position

	def __repr__(self):
		return "pos  [{:2d},{:2d}] : kind = {:12s}, value = {} \n".format(self.position[0], self.position[1], self.kind, self.value)
