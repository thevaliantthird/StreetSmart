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
    Y = X.GetRoadPixel()
    R = [TrafficInfer.RoadPix(x[0],x[1]) for x in Y]
    #print('Reached here!')

    det = predict.GetPredictions(Img[:,:,0:3])
    #print('Reached here!')
    B = [TrafficInfer.Building(det[i,:]) for i in range(det.shape[0])]
    #print('Reached here!')
    L+=TrafficInfer.Controller(B,R).GetDataSet()



    print('Completed Everything for this image!')
    print(len(L))

s = input('Name of file?')
with open(s,'wb') as f:
    np.save(f,np.array(L))
