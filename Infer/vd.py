import numpy as np
import math

class Rect:

    def __init__(self, vec, position, dim, traffic):
        self.vec = vec
        self.position = position
        self.dim = dim
        self.traffic = traffic

class Infer:

    def __init__(self, RectL, IMGDIM, TrafficMap):

        self.RectL = RectL
        self.IMGDIM = IMGDIM
        self.TrafficMap = TrafficMap
	
    def ConstructTraffic(self):
    
	    for i in range(self.IMGDIM[0]):
		    for j in range(self.IMGDIM[1]):
			    for k in self.RectL:

				    traffic = k.traffic
				    xk, yk = k.position
				    dist = math.sqrt((i-xk)**2 + (y-yk)**2)
				    contribution = traffic/dist

				    self.TrafficMap[i,j]+=contribution


    def ReduceNoise(self):
        
        for i in range(self.TrafficMap.shape[0]):
            for j in range(self.TrafficMap.shape[1]):
                for Rect in self.RectL:
                    if Rect.position == (i,j):
                        self.TrafficMap[(i-Rect.dim[0]/2):(i+Rect.dim[0]/2),(j-Rect.dim[0]/2):(j+Rect.dim[1]/2)] = 0
