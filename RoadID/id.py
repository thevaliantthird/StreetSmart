import numpy as np
import matplotlib.pyplot as plt


class RoadIdentifier:

	def __init__(self, ImagePath):

        	self.IMG = plt.imread(ImagePath)
        	self.ImageDIM = self.IMG.shape
        	self.MAT = np.zeros((self.ImageDIM[0],self.ImageDIM[1]))
        	self.marks = []
			process()
			DFS()


	def IfRoad(self,xs,ys):

		res = np.zeroes(4)
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


		#checking if there are 3 or more than three pixels having green color
		if(res.count(10)>=3):

			return 10 #green

		elif(res.count(40)>=3):

			return 40 #orange

		elif(res.count(80)>=3):

			return 80 #red

		elif(res.count(120)>=3):

			return 120 #brown

		else:

			return 0 #no route




	def process(self):

		for j in range(0,np.shape(self.IMG)[0],2):

			for i in range(0,np.shape(self.IMG[1])[1],2):

				col = IfRoad(i,j)

				self.MAT[i,j] = col
				self.MAT[i,j+1] = col
				self.MAT[i+1,j] = col
				self.MAT[i+1,j+1] = col

				self.marks.append((i,j))

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
	            if visit[x] is not 0:
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
	                	if ((y[0]+1,y[1]) in visit.keys()) and (visit[(y[0]+1,y[1])] is not 0) :
	                		todo.append((y[0]+1,y[1]))
	                	if ((y[0],y[1]+1) in visit.keys()) and (visit[(y[0],y[1]+1)] is not 0) :
	                		todo.append((y[0],y[1]+1))
	                	if ((y[0]-1,y[1]) in visit.keys()) and (visit[(y[0]-1,y[1])] is not 0) :
	                		todo.append((y[0]-1,y[1]))
	                	if ((y[0],y[1]-1) in visit.keys()) and (visit[(y[0],y[1]-1)] is not 0) :
	                		todo.append((y[0],y[1]-1))
	                	if ((y[0]+1,y[1]+1) in visit.keys()) and (visit[(y[0]+1,y[1]+1)] is not 0) :
	                		todo.append((y[0]+1,y[1]+1))
	                	if ((y[0]+1,y[1]-1) in visit.keys()) and (visit[(y[0]+1,y[1]-1)] is not 0) :
	                		todo.append((y[0]+1,y[1]-1))
	                	if ((y[0]-1,y[1]) in visit.keys()) and (visit[(y[0]-1,y[1])] is not 0) :
	                		todo.append((y[0]-1,y[1]))
	                	if ((y[0]-1,y[1]+1) in visit.keys()) and (visit[(y[0]-1,y[1]+1)] is not 0) :
	                		todo.append((y[0]-1,y[1]+1))
	                else:
	                	if (maxx < self.ImageDIM[0]-20) and  (maxy < self.ImageDIM[1]-20) and (minx >  20) and (miny >20) :
	                		for x in cat :
	                			self.MAT[x] = 0
