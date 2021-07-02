import TrafficInfer
import numpy as np

with open('Data.npy','rb') as f:
    D = np.load(f,allow_pickle = True)

D = list(D)
XI = []
YI = []

for y in D:
    X = []
    x = y.InputVec
    X.append(abs(x[2]-x[0]))
    X.append(abs(x[3]-x[1]))
    X+=list(np.zeros(10))
    X[2+int(x[-1])] = x[-2]
    XI.append(X)
    YI.append(y.Output)

with open('XI.npy','wb') as f:
    np.save(f,np.array(XI))

with open('YI.npy','wb') as f:
    np.save(f,np.array(YI))
