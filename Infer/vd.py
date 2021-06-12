import numpy as np
import math


class Road:
    def __init__(self, _length, starting, inclin, traff):
        self.length = _length
        self.StartingPoint = starting
        self.Inclination = inclin
        self.width = 0
        self.Traffic = traff


class RoadPointWeightageFromBuilding:
	def __init__ (self, traffic, road, building):
		self.Road = road
		self.Building  = building
		self.Traffic = traffic


class Rect:

    def __init__(self, vec, position, dim):
        self.vec = vec
        self.position = position
        self.dim = dim
        self.traffic = traffic
        self.RoadAdj = []


def GetDistance(X,Y):
    return math.sqrt(((X[0]-Y[0])*(X[0]-Y[0]))+((X[1]-Y[1])*(X[1]-Y[1])))

class Infer:

    def __init__(self, RectL, IMGDIM, TrafficMap):

        self.RectL = RectL
        self.IMGDIM = IMGDIM
        self.TrafficMap = TrafficMap
        self.Roads = []
        self.PixelToRoad = np.ones(IMGDIM)*(-1)
        self.PTRD = np.ones(IMGDIM)*(-1)
        self.StartPointforRoadTest = IMGDIM//2
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

    def PostulateRoads(self):
        return f


    def PixelToRoadMapping(self,neigh = 5):
        for i in range(0,len(self.Roads)):
            dx = int(math.cos(self.Roads[i].Inclination)*(self.Roads[i].length))
            sig = dx/abs(dx)
            for j in range(0,abs(dx)):
                for k in range(max(int((sig*j*math.tan(self.Roads[i].Inclination))-(neigh/2)),0),min(int((sig*j*math.tan(self.Roads[i].Inclination))+(neigh/2)),self.IMGDIM[1])):
                    self.PixelToRoad[int(self.Roads[i].StartingPoint[0]+(j*sig))][int(self.Roads[i].StartingPoint[1]+k)] = i
                    self.PTRD[int(self.Roads[i].StartingPoint[0]+(j*sig))][int(self.Roads[i].StartingPoint[1]+k)]  = i



    def IdentifyRoads(self):
    	#roadImpBuff = []
    	#for i in range(0,len(self.Roads)):
    	#	roadImpBuff.append([])
        for i in range(0,len(self.RectL)):
        	for x in range(max(int(self.RectL[i].position[0]-(self.RectL[i].vec[0]/2)-30),0),min(int(self.RectL[i].position[0]+(self.RectL[i].vec[0]/2)+30),self.IMGDIM[0])):
        		if x < int(self.RectL[i].position[0]-(self.RectL[i].vec[0]/2)) or x > int(self.RectL[i].position[0]+(self.RectL[i].vec[0]/2)):
        			for y in range(max(int(self.RectL[i].position[1]-(self.RectL[i].vec[1]/2)-30),0),min(int(self.RectL[i].position[1]+(self.RectL[i].vec[1]/2)+30),self.IMGDIM[1])):
        				if self.PixelToRoad[x][y] > -0.0001:
                            self.RectL[i].RoadAdj.append(self.PixelToRoad[x][y])
        					#roadImpBuff[int(self.PixelToRoad[x][y])].append(RoadPointWeightageFromBuilding(self.RectL[i].traffic/GetDistance(self.RectL[i].position,(x,y)),int(self.PixelToRoad[x][y]),i))
        		else:
        			for y in range(max(int(self.RectL[i].position[1]-(self.RectL[i].vec[1]/2)-30),0),min(int(self.RectL[i].position[1]-(self.RectL[i].vec[1]/2)),self.IMGDIM[1])):
        				if self.PixelToRoad[x][y] > -0.0001:
                            self.RectL[i].RoadAdj.append(self.PixelToRoad[x][y])
                            #roadImpBuff[int(self.PixelToRoad[x][y])].append(RoadPointWeightageFromBuilding(self.RectL[i].traffic/GetDistance(self.RectL[i].position,(x,y)),int(self.PixelToRoad[x][y]),i))
                    for y in range(max(int(self.RectL[i].position[1]+(self.RectL[i].vec[1]/2)),0),min(int(self.RectL[i].position[1]+(self.RectL[i].vec[1]/2)30)+30,self.IMGDIM[1])):
        				if self.PixelToRoad[x][y] > -0.0001:
                            self.RectL[i].RoadAdj.append(self.PixelToRoad[x][y])
                            #roadImpBuff[int(self.PixelToRoad[x][y])].append(RoadPointWeightageFromBuilding(self.RectL[i].traffic/GetDistance(self.RectL[i].position,(x,y)),int(self.PixelToRoad[x][y]),i))
        return roadImpBuff


    def FindAllInRadius(self,x, rad = 10):
        dime = self.IMGDIM
        res = []
        for i in range(int(x[0]-(rad/2)),int(x[0]+(rad/2))):
            for j in range(int(x[1]-(rad/2)),int(x[1]+(rad/2))):
                if self.PTRD[i][j] >-0.001:
                    res.append((i,j))
        return res


    def CheckFeasible(self, X, num):
        L = {}
        TODO = []
        TODO.append(X)
        while len(TODO)!=0:
            y = TODO.pop()
            L.add(self.PTRD[y[0]][y[1]])
            self.PTRD[y[0]][y[1]] = -1
            TODO+=FindAllInRadius(y)

        if len(L)<num
            return False
        else:
            return True

    def RemoveRoad(self, road):
        dx = int(math.cos(road.Inclination)*(road.length))
        sig = dx/abs(dx)
        for j in range(0,abs(dx)):
            for k in range(max(int((sig*j*math.tan(self.Roads[i].Inclination))-(neigh/2)),0),min(int((sig*j*math.tan(self.Roads[i].Inclination))+(neigh/2)),self.IMGDIM[1])):
                self.PTRD[int(road.StartingPoint[0]+(j*sig))][int(road.StartingPoint[1]+k)]  = -1

    def addRoadBack(self,road):
        dx = int(math.cos(road.Inclination)*(road.length))
        sig = dx/abs(dx)
        for j in range(0,abs(dx)):
            for k in range(max(int((sig*j*math.tan(self.Roads[i].Inclination))-(neigh/2)),0),min(int((sig*j*math.tan(self.Roads[i].Inclination))+(neigh/2)),self.IMGDIM[1])):
                self.PTRD[int(road.StartingPoint[0]+(j*sig))][int(road.StartingPoint[1]+k)]  = self.PixelToRoad[int(road.StartingPoint[0]+(j*sig))][int(road.StartingPoint[1]+k)]


    def UpdateOnACircle(self, C, R, traff):
        for i in range(0,360):
            x = max(min(int(R*math.cos(math.radians(i))+C[0]),self.IMGDIM[0]),0)
            y = max(min(int(R*math.sin(math.radians(i))+C[1]),self.IMGDIM[1]),0)
            self.TrafficMap[x][y] += traff/(R*R)


    def RemoveRoadAndNormalize(self,road):
        buildupdate = []
        rS = road.StartingPoint
        add = lambda x,y: (x[0]+y[0],x[1]+y[1])
        rE = add(rS,(road.length*math.cos(road.Inclination),road.length*math.sin(road.Inclination)))
        for i in range(0, len(self.RectL)):
            dx = int(math.cos(road.Inclination)*(road.length))
            sig = dx/abs(dx)
            for j in range(0,abs(dx)):
                for k in range(max(int((sig*j*math.tan(self.Roads[i].Inclination))-(neigh/2)),0),min(int((sig*j*math.tan(self.Roads[i].Inclination))+(neigh/2)),self.IMGDIM[1])):
                    UpdateOnACircle(self.RectL[i].position,GetDistance((j,k),self.RectL[i].position),self.RectL[i].traffic)

            dx = int(math.cos(road.Inclination)*(road.length))
            sig = dx/abs(dx)
            for j in range(0,abs(dx)):
                for k in range(max(int((sig*j*math.tan(self.Roads[i].Inclination))-(neigh/2)),0),min(int((sig*j*math.tan(self.Roads[i].Inclination))+(neigh/2)),self.IMGDIM[1])):
                    self.TrafficMap[j][k] = 0






    def ImproviseRoads(self,threshold = 50):
        lone = []
        justlist = []
        for i in range(0,len(self.RectL)):
            justlist.append(i)
            self.RectL[i].RoadAdj = list(set(self.RectL[i].RoadAdj))
            if len(self.RectL[i].RoadAdj)==1:
                lone.append(i)

        roadNum = len(self.Roads)
        lone = set(lone)
        lone = set(justlist)-lone
        rem = []
        for i in range(0,len(lone)):
            if self.Roads[lone[i]].Traffic < threshold:
                RemoveRoad(self.Roads[lone[i]])
                if CheckFeasible(self.StartPointforRoadTest,roadNum-1):
                    rem.append((self.Roads[i],i))
                    break
                else:
                    addRoadBack(self.Roads[lone[i]])
        if len(rem)==1:
            RemoveRoadAndNormalize(self.Roads[rem[0]])
            return True
        else:
            return False



    
