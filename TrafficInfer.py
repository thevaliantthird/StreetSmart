import numpy as np

class Building:
    def __init__(self, vec):
        self.vec = vec

class RoadPix:
    def __init__(self, _coordinate, _Traffic):
        self.coordinate = _coordinate
        self.Traffic = _Traffic
        self.buildlist = {}
        self.Z = 0

class DataSet:
    def __init__(self, inp, out):
        self.InputVec = inp
        self.Output = out



class Controller:
    def __init__(self, buildlist, roadlist):
        self.BuildingList = buildlist
        self.RoadPixels = roadlist
        self.DataList = []
        self.CreateDataset()

    def RoadIter(self, road, n):
        i = 0
        road.Z = 0
        while i<n:
            distance = ((self.BuildingList[i].vec[0] - road.coordinate[0])**2 + (self.BuildingList[i].vec[1] - road.coordinate[1])**2)**0.5
            road.Z += distance
            road.buildlist[i] = distance
            i += 1
        j = 0
        while j<n:
            road.buildlist[j] = float(road.buildlist[j])/road.Z
            j+=1
        return road

    def CreateDataset(self) :
        buildnum = [ 1 for i in range(0,len(self.BuildingList)) ]
        buildtraff = [ (0*i) for i in range(0,len(self.BuildingList)) ]
        Z = float(len(self.RoadPixels)*len(self.BuildingList))
        i = 0

        print(len(self.RoadPixels),len(self.BuildingList),Z)
        for x in self.RoadPixels:
            x = self.RoadIter(x,len(self.BuildingList))
            for key in range(0,len(self.BuildingList)):
                buildtraff[key]+=(x.buildlist[key])*x.Traffic
                buildnum[key]+=1
                i+=1
                #print(i)
        i = 0
        for x in self.BuildingList:
            self.DataList.append(DataSet(x.vec,buildtraff[i]/buildnum[i]))
            i+=1

    def GetDataSet(self):
        return self.DataList


def relu(x):

	if x>0:

		return x , x

	else:
		return 0 , x

def relu_backward(dA, activation_cache):

	if activation_cache < 0:

		return 0

	else:

		return dA


class Neural_Network:

	def __init__(self, inputarr, outputarr, layer_dims):

		self.X = inputarr
		self.Y = outputarr
		self.parameters = {}
		self.L = len(layer_dims)
		A=self.X
		self.caches = []
		self.AL=[]

		for l in range(1,L+1):

			self.parameters["W" + str(l)] = np.random.randn(layer_dims[l], layer_dims[l-1]) * 0.01
			self.parameters["b" + str(l)] = np.zeros((layer_dims[l],1))


	def linear_forward(A,W,b):

		z = np.dot(W, A) + b

		cache = (A,W,b)

		return Z, cache

	def linear_activation_forward(A_prev, W, b):

		Z, linear_cache = linear_forward(A_prev, W, b)
		A, activation_cache = relu(z)

		cache = (linear_cache, activation_cache)

	def l_model_forward(self):

		A = self.X

		for l in range(1, self.L):

			A_prev = A
			W, b = self.parameters['W'+str(l)], self.parameters['b'+str(l)]
			A, cache = linear_activation_forward(A_prev, W, b)
			self.caches.append(cache)

		self.AL = A #output layer

	def compute_cost(self):

		m = self.Y.shape[1]

		#assert (self.AL.shape()==self.Y.shape())

		cost = np.sum(np.power(self.AL-self.Y , 2)) / (2*m)

		cost = np.squeeze(cost)

		return cost


	def linear_backward(dZ, cache):

		A_prev, W, b= cache
		m = A_prev.shape[1]

		dw = np.dot(dZ, A_prev.T) / m
		db = np.sum(dZ, axis=1, keepdims=True) / m
		dA_prev = np.dot(W.T, dZ)

		return dA_prev, dW, db

	def linear_activation_backward (dA, cache):

		linear_cache, activation_cache = cache

		dZ = relu_backward(dA, activation_cache)
		dA_prev, dW, db = linear_backward(dZ, linear_cache)

		return dA_prev, dW, db

	def L_model_backward(self):

		self.grads={}
		m = self.AL.shape[1]
		Y = Y.reshape(AL.shape)

		dAL = np.sum(self.AL-self.Y) / m

		current_cache = self.caches[self.L-2]

		self.grads["dA" + str(L)], self.grads["dW" + str(L)], self.grads["db" + str(L)] = linear_activation_backward(dAL, current_cache)

		for l in reversed(range(self.L-2)):

			current_cache = self.caches[l]

			dA_prev, dW_temp, db_temp = linear_activation_backward(self.grads["dA"+str(l+2)], current_cache)

			self.grads["dA" + str(l + 1)] = dA_prev_temp
			self.grads["dW" + str(l + 1)] = dW_temp
			self.grads["db" + str(l + 1)] = db_temp


	def gradient_descent(self, learning_rate, num_iterations):

		for _ in range(num_iterations):

			for l in range (1, self.L+1):

				self.parameters["W" + str(l)] -= learning_rate * self.grads["dw" + str(l)]
				self.parameters["b" + str(l)] -= learning_rate * self.grads["db" + str(l)]
