import numpy as np

class Collection:

    def __init__(self,pixels,boundary,label):
        self.pixels = pixels
        self.boundary = boundary
        self.label = label

class RoadParsing:

    list_col = []

    def __init__(self, image):
        self.image = image
        self.bool_pxls = (image == 0).astype(int)

    def process(self):
        label = 1
        visited = set()
        print(self.bool_pxls)
        for i in range(self.bool_pxls.shape[0]):
            for j in range(self.bool_pxls.shape[1]):
                if(self.bool_pxls[i,j] == 1) and (i,j) not in visited:
                    col= set()
                    boundary = set()
                    self.DFS(self.bool_pxls,(i,j),visited,col,boundary)
                    # print("visited: ", visited)
                    # print("col: ", col)
                    # print("boundary: ", boundary)
                    self.list_col.append(Collection(col,boundary,label))
                    label+=1

    def RoadIter(Controller main, RoadPix road, int n):
    i = 0
    road.Z = 0
    while i<n:
        distance = ((main.BuildingList[i].Shape.x - road.coordinate.x)**2 + (main.BuildingList[i].Shape.y - road.coordinate.y)**2)**0.5
        road.Z += distance
        road.buildlist[i] = distance
        i += 1
    j = 0
    while j<n:
        road.buildlist[j] = float(road.buildlist[j])/road.Z

    

    def DFS(self, pixels, node, visited, col, boundary):
        if node not in visited:
            print(node)
            visited.add(node)
            col.add(node)
            if self.isboundary(node,pixels): boundary.add(node)

            if node[0] != pixels.shape[0]-1 and (pixels[node[0]+1,node[1]] == 1):
                self.DFS(pixels, (node[0]+1, node[1]),visited,col,boundary)
            if node[1] != pixels.shape[1]-1 and (pixels[node[0],node[1]+1] == 1):
                self.DFS(pixels, (node[0], node[1]+1),visited,col,boundary)
            if node[0] != 0 and (pixels[node[0]-1,node[1]] == 1):
                self.DFS(pixels, (node[0]-1, node[1]),visited,col,boundary)
            if node[1] != 0 and (pixels[node[0],node[1]-1] == 1):
                self.DFS(pixels, (node[0], node[1]-1),visited,col,boundary)

    def isboundary(self,node,pixels):
        if(node[0] == 0 or node[0] == pixels.shape[0]-1 or node[1] == 0 or node[1] == pixels.shape[1]-1 ): return True
        if(pixels[node[0]+1,node[1]] == 0 or pixels[node[0],node[1]+1] == 0 or pixels[node[0]-1,node[1]]== 0 or pixels[node[0], node[1]-1] == 0): return True
        if(pixels[node[0]+1,node[1]+1] == 0  or pixels[node[0]+1,node[1]-1] == 0  or pixels[node[0]-1,node[1]+1] == 0 or pixels[node[0]-1, node[1]-1] == 0): return True
        return False
