roadmatrixfinal = roadmatrix
roadmatrixcopy = roadmatrix
def PostulationToRoads(roadmatrix, roadmatrixfinal, m, n):
    i = 0
    j = 0
    k = 0
    roadmatrixT = roadmatrix
    roadmatrixfinal = roadmatrix
    while i < m:
        while j < n:
            if (roadmatrix[i][j] > 0) or (k > j + 1):
                k = min(max(j + roadmatrix[i][j] + 1, k), n)
                roadmatrix[i][j] = 1
                j += 1
            else:
                j += 1
        j = 0
        i += 1
    j = 0
    i = 0
    k = 0
    while j < n:
        while i < m:
            if (roadmatrixT[i][j] > 0) || (k > i + 1):
                k = min(max(i + roadmatrixT[i][j] + 1, k), n)
                roadmatrixT[i][j] = 1
                i += 1
            else:
                i += 1
        i = 0
        j += 1
    i = 0
    j = 0
    while i < m:
        while j < n:
            if (roadmatrix[i][j] == 1) || (roadmatrixT[i][j] == 1):
                roadmatrixfinal[i][j] = 1
            else:
                roadmatrixfinal[i][j] = 0
            j += 1
        j = 0
        i += 1
