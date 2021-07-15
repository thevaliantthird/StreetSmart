import numpy as np
import matplotlib.pyplot as plt

def Vizualize(data,str):
    A = np.zeros((data.shape[0],data.shape[1],3))
    im = (data > 0000).astype(float)
    im = np.dstack((np.dstack((im,im)),im))
    plt.imsave(str+'.png',im)
