import numpy as np
import matplotlib.pyplot as plt


class RoadIdentifier :

    def __init__(self, ImagePath):

        self.IMG = plt.imread(ImagePath)
        self.ImageDIM = self.IMG.shape
        self.MAT = np.zeros((self.ImageDIM[0],self.ImageDIM[1]))
        self.marks = []

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
