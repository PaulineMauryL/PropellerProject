class BladePart:
	"""Class to represent blade of propeller alone"""


	def __init__(self, X, Y, Z) :
		self._x = X
		self._y = Y
		self._z = Z

	def _get_x(self) :
		return self.x
	def _set_x(self, new_x) :
		print("Warning: Updating x coordinates")
		self._x = new_x
	x = property(_get_x, _set_x)

	def _get_y(self) :
		return self.y
	def _set_y(self, new_y) :
		print("Warning: Updating y coordinates")
		self._y = new_y
	y = property(_get_y, _set_y)

	def _get_z(self) :
		return self.z
	def _set_z(self, new_z) :
		print("Warning: Updating z coordinates")
		self._z = new_z
	z = property(_get_z, _set_z)

	def __repr__(self) :
		return "x is {} \n\n y is {} \n\n z is {} \n\n ".format(self.x, self.y, self.z)
