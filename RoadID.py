import numpy as np
import matplotlib.pyplot as plt


def PrintImage(Img,s):
    X = np.zeros((Img.shape[0],Img.shape[1],4))
    for i in range(0,Img.shape[0]):
        for j in range(0,Img.shape[1]):
            X[i,j,0] = float(Img[i,j])/240.0
            X[i,j,1] = float(Img[i,j])/240.0
            X[i,j,2] = float(Img[i,j])/240.0
            X[i,j,3] = 1.0
    plt.imsave(s+'.png',X)



class RoadIdentifier:

	def __init__(self, Image):
		self.IMG = Image[:,:,0:3]
		self.ImageDIM = self.IMG.shape
		self.MAT = np.zeros((self.ImageDIM[0],self.ImageDIM[1]))
		self.marks = []
		self.process()



	def IfRoad(self,xs,ys):

		res = np.zeros(4)
		ct=0

		for i in range(2):
			for j in range(2):

				col = self.IMG[xs+i,ys+j]


				#RED
				if (0.9<=col[0]<=1 and 0.0<=col[1]<=0.2 and 0.2<=col[2]<=0.3):

					res[ct]=80


				#GREEN
				elif (0.0<=col[0]<=0.2 and 0.85<=col[1]<=0.92 and 0.32<=col[2]<=0.39):

					res[ct]=10


				#ORANGE
				elif (0.82<=col[0]<=1 and 0.4<=col[1]<=0.6 and 0.18<=col[2]<=0.33):

					res[ct]=40


				#BROWN
				elif (0.65<=col[0]<=0.75 and 0.0<=col[1]<=0.1 and 0.0<=col[2]<=0.1):

					res[ct]=120

				ct+=1


		#checking if there are 3 or more than three self.bool_pxls having green color
		res = list(res)
		if(res.count(10)>=2):

			return 10.0 #green

		elif(res.count(40)>=2):

			return 40.0 #orange

		elif(res.count(80)>=2):

			return 80.0 #red

		elif(res.count(120)>=2):

			return 120.0 #brown

		else:

			return 0.0 #no route




	def process(self):

		for i in range(0,np.shape(self.IMG)[0],2):
			if i==self.IMG.shape[0]-1:
				break
			for j in range(0,np.shape(self.IMG)[1],2):
				if j==self.IMG.shape[1]-1:
					break
				col = self.IfRoad(i,j)
				self.MAT[i,j] = col
				if col > 5:
					self.marks.append(((i,j),col))

	def DFS(self):

		visit = {}
		todo = []
		i = 1
		for x in self.marks:
			visit[x] = i
			y = (x[0]+1,x[1])
			visit[y] = i
			y = (x[0],x[1]+1)
			visit[y] = i
			y = (x[0]+1,x[1]+1)
			visit[y] = i
			i+=1
		for x in self.marks:
			if visit[x]!=0:
				cat = []
				maxx = -1
				minx = 1000000000
				miny = 1000000000
				maxy = -1
				todo.append(x)
				while len(todo) != 0:
					y = todo.pop()
					visit[y] = 0
					if y[0]>maxx:
						maxx = y[0]
					if y[1] > maxy:
						maxy = y[1]
					if y[0] < minx:
						minx = y[0]
					if y[1] < miny:
						miny = y[1]
					cat.append(y)
					if ((y[0]+1,y[1]) in visit.keys()) and (visit[(y[0]+1,y[1])] != 0) :
						todo.append((y[0]+1,y[1]))


	def GetRoadPixel(self):
		return self.marks



class Collection:

    def __init__(self,boundary,label,maXX,maXY):
        self.boundary = boundary
        self.label = label
        minX = maXX
        minY = maXY
        maxX = 0
        maxY = 0
        for (x,y) in boundary:
            maxX = max(maxX,x)
            minX = min(minX,x)
            minY = min(minY,y)
            maxY = max(maxY,y)
        self.XU = maxX
        self.XL = minX
        self.YU = maxY
        self.YL = minY
        Roads = []
    def GetRectBoundary(self):
        return (self.XL,self.XU,self.YL,self.YU)

    def GetBoundary(self):
        return self.boundary



class RoadParsing:

	def __init__(self, image):

		self.list_col = []
		self.image = image
		self.bool_pxls = (image < 5).astype(int)
		self.visited = np.zeros(self.bool_pxls.shape)
		self.boundary = []
		self.process()

	def GetListCol(self):
		return self.list_col

	def process(self):
		label = 1
    #    print(self.bool_pxls)
		for i in range(self.bool_pxls.shape[0]):
			for j in range(self.bool_pxls.shape[1]):
				if(self.bool_pxls[i,j] == 1) and self.visited[i,j]==0:
					self.boundary = set()
					self.DFS((i,j))
					#print("boundary: ", self.boundary)
					self.list_col.append(Collection(list(self.boundary),label,self.bool_pxls.shape[0],self.bool_pxls.shape[1]))
					label+=1


	def DFS(self, node):
		todo = []
		todo.append(node)
		while len(todo)!=0:
			x = todo.pop()
			if self.isboundaryA(x) or self.isboundaryB(x):
				self.boundary.add(x)
			if self.isboundaryB(x)==False and self.visited[x[0],x[1]]==0:
				self.visited[x[0],x[1]] = 1
				if (x[0] != (self.bool_pxls.shape[0]-1)) and (self.bool_pxls[x[0]+1,x[1]] == 1) :
					todo.append((x[0]+1, x[1]))
				if x[1] != self.bool_pxls.shape[1]-1 and (self.bool_pxls[x[0],x[1]+1] == 1):
					todo.append((x[0], x[1]+1))
				if x[0] != 0 and (self.bool_pxls[x[0]-1,x[1]] == 1):
					todo.append((x[0]-1, x[1]))
				if x[1] != 0 and (self.bool_pxls[x[0],x[1]-1] == 1):
					todo.append((x[0], x[1]-1))

	def isboundaryA(self,node):
		if node[0] <= 0 or node[0] >= (self.bool_pxls.shape[0]-1) or node[1] <= 0 or node[1] >= (self.bool_pxls.shape[1]-1) : return True
		return False
	def isboundaryB(self,node):
		if self.bool_pxls[node[0],node[1]]==0: return True
		return False
