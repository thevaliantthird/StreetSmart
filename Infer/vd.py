# traffic infer
import numpy as np

class Rect:

	def __init__:
		
		self.vec = []
		self.position = [0,0]
		self.dim = [0,0]
		self.traffic = 0

class Roads:

	def __init__:

		self.length = 0
		self.width = 0

class Infer:

	def __init__:

		self.RectL = []
		self.IMGDIM = [0,0]
		self.TrafficMap = np.zeros(self.IMGDIM)

	
	def ConstructTraffic():

		for i in range(self.IMGDIM[0]):
			for j in range(self.IMGDIM[0]):
				for k in self.RectL:

					traffic = k.traffic
					xk, yk = k.position
					dist = math.sqrt((i-xk)**2 + (y-yk)**2)
					contribution = traffic/dist

					self.TrafficMap[i,j]+=contribution
