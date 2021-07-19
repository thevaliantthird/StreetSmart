import numpy as np
import matplotlib.pyplot as plt


def Vizualize(data1,data2,x,str):
    data1 = (data1 > (np.mean(data1)+(x*np.std(data1)))).astype(float)
    data2 = (data2 > np.mean(data2)+(x*np.std(data2))).astype(float)
    im = ((data1+data2 > 0).astype(float)).T
    im = np.dstack((np.dstack((im,im)),im))
    print(im.shape)
    plt.imsave(str+'.png',1.00-im)

with open('TrafficHA.npy','rb') as f:
	H = np.load(f)

with open('TrafficVA.npy','rb') as f:
	V = np.load(f)

Vizualize(H,V,0,'tests/0')

for i in range(1,11):
	Vizualize(H,V,1+(i/10),'tests/'+str(i*10000))


