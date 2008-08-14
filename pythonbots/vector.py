import math

def _is_numeric(obj):
	if isinstance(obj, (int, long, float)):
		return True
	else:
		return False

class Vector(object):

	def __init__(self, a=0, b=0 ):
		if _is_numeric(a):
			#assume two numbers
			self.x = a
			self.y = b
		else:
			#assume Vectors/tuples
			self.x = b[0] - a[0]
			self.y = b[1] - a[1]

	def __getitem__(self, index):
		if index == 0:
			return self.x
		elif index == 1:
			return self.y
		else:
			raise IndexError
		
	def __add__(self, other):
		return Vector(self.x + other.x, self.y + other.y)

	def __sub__(self, other):
		return Vector(self.x - other.x, self.y - other.y)

	def __mul__(self, other):
		try:
			other = other - 0
		except:
			raise TypeError, "Only scalar multiplication is supported."
		return Vector( other * self.x, other * self.y )

	def __rmul__(self, other):
		return self.__mul__(other)
		
	def __div__(self, other):
		return Vector( self.x / other, self.y / other )

	def __neg__(self):
		return Vector(-self.x, -self.y)

	def __abs__(self):
		return self.length()
	
	def __repr__(self):
		return '(%s, %s)' % (self.x, self.y)

	def __str__(self):
		return '(%s, %s)' % (self.x, self.y)

	def dot(self, vector):
		return self.x * vector.x + self.y * vector.y

	def cross(self, vector):
		return self.x * vector.y - self.y * vector.x

	def length(self):
		return math.sqrt( self.dot(self) )

	def perpindicular(self):
		return Vector(-self.y, self.x)

	def unit(self):
		return self / self.length()
	
	def projection(self, vector):
		k = (self.dot(vector)) / vector.length()
		return k * vector.unit()

	def angle(self, vector=None):
		if vector == None:
			vector = Vector(1,0)
		return math.acos((self.dot(vector))/(self.length() * vector.length()))

	def angle_in_degrees(self, vector=None):
		return (self.angle(vector) * 180) /math.pi


