import numpy as np

class Building:
    def __init__(self, shape, vec):
        self.shape = shape
        self.vec = vec

class RoadPix:
    def __init__(self, _coordinate, _Traffic):
        self.coordinate = _coordinate
        self.Traffic = _Traffic
        self.buildlist = {}
        self.Z = 0

class DataSet:
    def __init__(self, inp, out):
        self.InputVec
        self.Output


class Controller:
    def __init__(self, buildlist, roadlist, trafficlist, DIM):
        self.BuildingList = buildlist
        self.RoadPixels = [ RoadPix(roadlist[i],trafficlist[i]) for i in range(0,len(roadlist))]
        self.ImageDIM = DIM
        self.DataList = []

    def CreateDataset(self) :
        buildnum = [ (0*i) for i in range(0,len(BuildingList)) ]
        buildtraff = [ (0*i) for i in range(0,len(BuildingList)) ]

        for x in self.RoadPixels:
            for key in x.buildlist.keys():
                buildtraff[key]+=(x.buildlist[key])*x.Traffic
                buildnum[key]+=1
        i = 0
        for x in BuildingList:
            self.DataList.append(DataSet(np.hstack((x.shape,x.vec),buildtraff[i]/buildnum[i])))
            
