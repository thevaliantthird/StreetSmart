roadwidth = np.empty(n*m)
roadXcoordinate = np.empty(n*m)
roadYcoordinate = np.empty(m*n)
roadwidthT = np.empty(n*m)
roadXcoordinateT = np.empty(n*m)
roadYcoordinateT = np.empty(m*n)

def setWidth(roadmatrixcopy, roadmatrixfinal, roadwidth, roadwidthT, roadXcoordinate, roadXcoordinateT, roadYcoordinate, roadYcoordinateT, m, n):
    roadwidth = np.empty(n*m)
    roadXcoordinate = np.empty(n*m)
    roadYcoordinate = np.empty(m*n)
    roadsum = 0
    length = 0
    i = 0
    j = 0
    k = 0
    while i < m:
        while j < n:
            if roadmatrixfinal[i][j] == 1:
                if  (j = 0 || roadmatrixcopy[i][j-1] == 0):
                    roadXcoordinate[k] = i
                    roadYcoordinate[k] = j
                roadsum += roadmatrixcopy[i][j]
                length += 1
            if roadmatrixfinal[i][j] == 0 && j != 0 && roadmatrixfinal[i][j-1] == 1:
                roadwidth[k] = roadsum/length
                k += 1
            j += 1
        j = 0
        i += 1
    roadwidthT = np.empty(n*m)
    roadXcoordinateT = np.empty(n*m)
    roadYcoordinateT = np.empty(m*n)
    roadsum = 0
    length = 0
    i = 0
    j = 0
    k = 0
    while j < n:
        while i < m:
            if roadmatrixfinal[i][j] == 1:
                if  (i = 0 || roadmatrixcopy[i-1][j] == 0):
                    roadXcoordinateT[k] = i
                    roadYcoordinateT[k] = j
                roadsum += roadmatrixcopy[i][j]
                length += 1
            if roadmatrixfinal[i][j] == 0 && i != 0 && roadmatrixfinal[i-1][j] == 1:
                roadwidthT[k] = roadsum/length
                k += 1
            i += 1
        i = 0
        j += 1
    
