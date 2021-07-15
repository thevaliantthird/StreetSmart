import numpy as np
import math as m
import pickle

def relu(z):
    return (z>0)*z , z

def linear(z):
    return z,z

def relu_backward(dA,z):
    return dA*((z>0).astype(float))

def Linear_backward(dA,z):
    return dA
def Huber(AL,Y):
    return np.multiply((np.abs(Y-AL) <=100000),(1/2)*np.multiply(Y-AL,Y-AL)) + (np.abs(AL-Y) - 50000)*100000

def HuberD(AL,Y):
    return np.multiply((np.abs(Y-AL) <=100000),AL-Y) + np.multiply((AL-Y>10000).astype(float)+((AL-Y<-10000).astype(float))*(-1),100000)

def MAEWeightedLossDet(AL,Y):
    return np.multiply(((AL>Y).astype(float)),(1/np.abs(Y))) + np.multiply(((AL<Y).astype(float)),(-1/np.abs(Y)))

def initialize_parameters_deep(layer_dims):

    np.random.seed(3)
    parameters = {}
    L = len(layer_dims)
    for l in range(1, L):

        parameters['W' + str(l)] = np.random.randn(layer_dims[l-1],layer_dims[l])
        parameters['b' + str(l)] = np.zeros((1,layer_dims[l]))

        assert(parameters['W' + str(l)].shape == (layer_dims[l-1], layer_dims[l]))
        assert(parameters['b' + str(l)].shape == (1,layer_dims[l]))


    return parameters


def linear_forward(A, W, b):

    Z = np.dot(A,W)+b

    assert(Z.shape == (A.shape[0], W.shape[1]))
    cache = (A, W, b)

    return Z, cache

def linear_activation_forward(A_prev, W, b, activation):


    if activation == "sigmoid":
        Z, linear_cache = linear_forward(A_prev,W,b)
        A, activation_cache = sigmoid(Z)

    elif activation == "relu":

        Z, linear_cache = linear_forward(A_prev,W,b)
        A, activation_cache = relu(Z)
    elif activation =="linear":
        Z, linear_cache = linear_forward(A_prev,W,b)
        A, activation_cache = linear(Z)

    cache = (linear_cache, activation_cache)

    return A, cache

def L_model_forward(X, parameters):

    caches = []
    A = X
    L = len(parameters) // 2                  # number of layers in the neural network

    for l in range(1, L):
        A_prev = A

        A, cache = linear_activation_forward(A_prev,parameters['W'+str(l)],parameters['b' + str(l)],"relu")
        caches.append(cache)



    AL, cache = linear_activation_forward(A,parameters['W'+str(L)],parameters['b'+str(L)],"linear")
    caches.append(cache)



    return AL, caches

def compute_cost(AL, Y):

    global m
    cost = (1/m)*np.sum(np.multiply((AL-Y),(AL-Y)))
    return cost

def linear_backward(dZ, cache):

    A_prev, W, b = cache
    m = A_prev.shape[0]

    dW = 1/m*np.dot(A_prev.T,dZ)
    db =  1/m*(np.sum(dZ,axis=0, keepdims=True))
    dA_prev = np.dot(dZ,W.T)

    # print(type(dZ))
    # print(b.shape)
    # print(A_prev.shape)
    # print(W.shape)
    # print(dW.shape)
    # print(db.shape)
    # print(dA_prev.shape)

    assert (dA_prev.shape == A_prev.shape)
    assert (dW.shape == W.shape)
    assert (db.shape == b.shape)

    return dA_prev, dW, db

def linear_activation_backward(dA, cache, activation):

    linear_cache, activation_cache = cache

    if activation == "relu":

        dZ = relu_backward(dA,activation_cache)
        dA_prev, dW, db = linear_backward(dZ,linear_cache)

    elif activation == "linear":
        dZ = Linear_backward(dA,activation_cache)
        dA_prev, dW, db = linear_backward(dZ,linear_cache)

    return dA_prev, dW, db


def L_model_backward(AL, Y, caches):

    grads = {}
    L = len(caches) # the number of layers
    global m
    Y = Y.reshape(AL.shape) # after this line, Y is the same shape as AL

    # Initializing the backpropagation
    dAL = 2*(AL-Y)


    # Lth layer (SIGMOID -> LINEAR) gradients. Inputs: "AL, Y, caches". Outputs: "grads["dAL"], grads["dWL"], grads["dbL"]

    current_cache = caches[L-1]
    grads["dA" + str(L)], grads["dW" + str(L)], grads["db" + str(L)] = linear_activation_backward(dAL,current_cache,"linear")


    for l in reversed(range(L-1)):
        # lth layer: (RELU -> LINEAR) gradients.
        # Inputs: "grads["dA" + str(l + 2)], caches". Outputs: "grads["dA" + str(l + 1)] , grads["dW" + str(l + 1)] , grads["db" + str(l + 1)]

        current_cache = caches[l]
        dA_prev_temp, dW_temp, db_temp = linear_activation_backward(grads["dA"+str(l+2)],current_cache,"relu")
        grads["dA" + str(l + 1)] = dA_prev_temp
        grads["dW" + str(l + 1)] = dW_temp
        grads["db" + str(l + 1)] = db_temp

    return grads

def L_model_backwardAction(AL, Y, caches):

    grads = {}
    L = len(caches) # the number of layers
    Y = Y.reshape(AL.shape) # after this line, Y is the same shape as AL

    # Initializing the backpropagation
    dAL = np.array([[-100000.00]])


    # Lth layer (SIGMOID -> LINEAR) gradients. Inputs: "AL, Y, caches". Outputs: "grads["dAL"], grads["dWL"], grads["dbL"]

    current_cache = caches[L-1]
    grads["dA" + str(L)], grads["dW" + str(L)], grads["db" + str(L)] = linear_activation_backward(dAL,current_cache,"linear")


    for l in reversed(range(L-1)):
        # lth layer: (RELU -> LINEAR) gradients.
        # Inputs: "grads["dA" + str(l + 2)], caches". Outputs: "grads["dA" + str(l + 1)] , grads["dW" + str(l + 1)] , grads["db" + str(l + 1)]

        current_cache = caches[l]
        dA_prev_temp, dW_temp, db_temp = linear_activation_backward(grads["dA"+str(l+2)],current_cache,"relu")
        grads["dA" + str(l + 1)] = dA_prev_temp
        grads["dW" + str(l + 1)] = dW_temp
        grads["db" + str(l + 1)] = db_temp

    return grads


def initialize_adam(parameters) :


    L = len(parameters) // 2 # number of layers in the neural networks
    v = {}
    s = {}

    # Initialize v, s. Input: "parameters". Outputs: "v, s".
    for l in range(L):
        v["dW" + str(l+1)] = np.zeros(parameters['W' + str(l+1)].shape)
        v["db" + str(l+1)] = np.zeros(parameters['b' + str(l+1)].shape)
        s["dW" + str(l+1)] = np.zeros(parameters['W' + str(l+1)].shape)
        s["db" + str(l+1)] = np.zeros(parameters['b' + str(l+1)].shape)


    return v, s

def update_parameters_with_adam(parameters, grads, v, s, t, learning_rate=0.001,
                                beta1=0.7, beta2=0.75, epsilon=1e-8):

        L = len(parameters) // 2                 # number of layers in the neural networks
        v_corrected = {}                         # Initializing first moment estimate, python dictionary
        s_corrected = {}                         # Initializing second moment estimate, python dictionary

        # Perform Adam update on all parameters
        for l in range(L):
            # Moving average of the gradients. Inputs: "v, grads, beta1". Output: "v".

            v["dW" + str(l + 1)] = beta1 * v["dW" + str(l + 1)] + (1 - beta1) * grads['dW' + str(l + 1)]
            v["db" + str(l + 1)] = beta1 * v["db" + str(l + 1)] + (1 - beta1) * grads['db' + str(l + 1)]


            # Compute bias-corrected first moment estimate. Inputs: "v, beta1, t". Output: "v_corrected".

            v_corrected["dW" + str(l + 1)] = v["dW" + str(l + 1)] / (1 - np.power(beta1, t))
            v_corrected["db" + str(l + 1)] = v["db" + str(l + 1)] / (1 - np.power(beta1, t))


            # Moving average of the squared gradients. Inputs: "s, grads, beta2". Output: "s".

            s["dW" + str(l + 1)] = beta2 * s["dW" + str(l + 1)] + (1 - beta2) * np.power(grads['dW' + str(l + 1)], 2)
            s["db" + str(l + 1)] = beta2 * s["db" + str(l + 1)] + (1 - beta2) * np.power(grads['db' + str(l + 1)], 2)


            # Compute bias-corrected second raw moment estimate. Inputs: "s, beta2, t". Output: "s_corrected".

            s_corrected["dW" + str(l + 1)] = s["dW" + str(l + 1)] / (1 - np.power(beta2, t))
            s_corrected["db" + str(l + 1)] = s["db" + str(l + 1)] / (1 - np.power(beta2, t))


            # Update parameters. Inputs: "parameters, learning_rate, v_corrected, s_corrected, epsilon". Output: "parameters".

            parameters["W" + str(l + 1)] = parameters["W" + str(l + 1)] - (learning_rate * v_corrected["dW" + str(l + 1)]) / (np.sqrt(s_corrected["dW" + str(l + 1)]) + epsilon)
            parameters["b" + str(l + 1)] = parameters["b" + str(l + 1)] - (learning_rate * v_corrected["db" + str(l + 1)]) / (np.sqrt(s_corrected["db" + str(l + 1)]) + epsilon)


        return parameters, v, s


#
# with open('param.soc','wb') as f:
#     pickle.dump(Parameters,f)
# cal = 0
# with open('param500.soc','rb') as f:
#     pra = pickle.load(f)
#
# for j in range(0,10):
#     al, cac = L_model_forward(X[11296*j:11296*(j+1)],Parameters)
#
#     cal += compute_cost(al,Y[11296*j:11296*(j+1)])
#
# print(cal)
