import RoadID
import TrafficInfer
import predict
import numpy as np
import matplotlib.pyplot as plt
import sys

sys.setrecursionlimit(10**6)


L = []

x = int(input('Starting Image from which you would like to start the training?'))
y = int(input('The Last Image till which you would like to do the training?'))

for i in range(x,y+1):
    print('Processing started for the', i, 'th image!')
    Img = plt.imread('images/'+str(i)+'.png')
    X = RoadID.RoadIdentifier(Img)
    print('Roads Identified!')
    Y = X.GetImageMAT()
    X = RoadID.RoadParsing(Y)
    print('Roads Parsed!')
    X = X.GetListCol()
    print('Boundaries and Sections Identified! A total of ', len(X),' such structures were Identified!')
    i = 0
    for y in X:
        print('Starting Processing for the ',i,'th Cluster.')
        J = y.GetBoundary()
        J1 = []
        for t in J:
            if Y[t[0],t[1]] != 0:
                J1.append(RoadPix(t,Y[t[0],t[1]]))
        R = y.GetRectBoundary()
        if (R[1]-R[0]) >= 2 and (R[3]-R[2])>=2 :
            det = predict.GetPredictions(Img[R[0]:R[1],R[2]:R[3],0:3])
            BL = [TrafficInfer.Building(det[i,:]) for i in range(0,det.shape[0])]
            L+=TrafficInfer.Controller(BL,J1).GetDataSet()
        i+=1
    print('Completed Everything for this image!')
    print(len(L))

s = input('Name of file?')
with open(s,'wb') as f:
    np.save(f,np.array(L))
