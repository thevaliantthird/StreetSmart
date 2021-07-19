import numpy as np
import math


class Rect:

    def __init__(self, position, dim,traffic):
        self.position = position
        self.dim = dim  #0 is length
        self.traffic = traffic



class Infer:

    def __init__(self, RectL, IMGDIM):
        self.RectL = RectL
        self.IMGDIM = IMGDIM
        self.TrafficMapH = np.zeros(IMGDIM)
        self.TrafficMapV = np.zeros(IMGDIM)
        self.TrafficMap = np.zeros(IMGDIM)
        self.ConstructTraffic()
        self.ReduceNoise()
        self.RLForTraffic(np.std(self.TrafficMap)*1.5)
        

    def ConstructTraffic(self):

        for i in range(0,self.IMGDIM[1]):
            for k in self.RectL:
                traff = k.traffic + 10
                xk, yk = k.position
                if i < yk-(k.dim[1]/2):
                    self.TrafficMapH[:,i]+=(traff/abs(i-yk))*np.ones(self.IMGDIM[0])
                if i > yk + (k.dim[1]/2):
                    self.TrafficMapH[:,i]+=(traff/abs(i-yk))*np.ones(self.IMGDIM[0])

        for i in range(0,self.IMGDIM[0]):
           for k in self.RectL:
                traff = k.traffic + 10
                xk, yk = k.position
                if i < xk-(k.dim[0]/2):
                    self.TrafficMapV[i,:]+=(traff/abs(i-xk))*np.ones(self.IMGDIM[1])
                if i > xk + (k.dim[0]/2):
                    self.TrafficMapV[i,:]+=(traff/abs(i-xk))*np.ones(self.IMGDIM[1])




    def ReduceNoise(self):
        for Rect in self.RectL:
            self.TrafficMapH[int(Rect.position[0]-(Rect.dim[0]/2)):int(Rect.position[0]+(Rect.dim[0]/2)),int(Rect.position[1]-(Rect.dim[1]/2)):int(Rect.position[1]+(Rect.dim[1]/2))] = 0
            self.TrafficMapV[int(Rect.position[0]-(Rect.dim[0]/2)):int(Rect.position[0]+(Rect.dim[0]/2)),int(Rect.position[1]-(Rect.dim[1]/2)):int(Rect.position[1]+(Rect.dim[1]/2))] = 0
        self.TrafficMap = self.TrafficMapH+self.TrafficMapV

    def RLForTraffic(self, threshold):
        for i in range(self.IMGDIM[0]):
            if np.mean(self.TrafficMap[i,:]) < threshold:
                t = 0
                for k in self.RectL:
                    traff = k.traffic + 10
                    xk, yk = k.position
                    if i < xk-(k.dim[0]/2):
                        self.TrafficMapV[i,:]-=(traff/abs(i-xk))*np.ones(self.IMGDIM[1])
                        g = min(self.IMGDIM[0]-1,int(i+abs(i-xk)))
                        self.TrafficMapV[g,:]+=(traff/abs(i-xk))*np.ones(self.IMGDIM[1])
                        t+=1
                    if i > xk + (k.dim[0]/2):
                        self.TrafficMapV[i,:]-=(traff/abs(i-xk))*np.ones(self.IMGDIM[1])
                        g = max(0,int(i-abs(i-xk)))
                        self.TrafficMapV[g,:]+=(traff/abs(i-xk))*np.ones(self.IMGDIM[1])
                        t+=1
                if t > 0:
                    self.ReduceNoise()
        for i in range(self.IMGDIM[1]):
            if np.mean(self.TrafficMap[:,i]) < threshold:
                t = 0
                for k in self.RectL:
                    traff = k.traffic + 10
                    xk, yk = k.position
                    if i < yk-(k.dim[1]/2):
                        self.TrafficMapV[:,i]-=(traff/abs(i-yk))*np.ones(self.IMGDIM[0])
                        g = min(self.IMGDIM[1]-1,int(i+abs(i-yk)))
                        self.TrafficMapV[:,g]+=(traff/abs(i-yk))*np.ones(self.IMGDIM[0])
                        t+=1
                    if i > yk + (k.dim[1]/2):
                        self.TrafficMapV[:,i]-=(traff/abs(i-yk))*np.ones(self.IMGDIM[0])
                        g = max(0,int(i-abs(i-yk)))
                        self.TrafficMapV[:,g]+=(traff/abs(i-yk))*np.ones(self.IMGDIM[0])
                        t+=1
                if t>0:
                    self.ReduceNoise()
