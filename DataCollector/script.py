import matplotlib.pyplot as plt
import os

start = int(input("Enter the number from which you'd like to start the selection Process?"))
end = int(input("Enter the number, till which you would want to do it?"))
xl = [0,0,0,0,0,0,0,0,0,0]
xl[0] = int(input("Input the number from where enumeration will start in 0th class: "))
xl[1] = int(input("Input the number from where enumeration will start in 1st class: "))
xl[2] = int(input("Input the number from where enumeration will start in 2nd class: "))
xl[3] = int(input("Input the number from where enumeration will start in 3rd class: "))
xl[4] = int(input("Input the number from where enumeration will start in 4th class: "))
xl[5] = int(input("Input the number from where enumeration will start in 5th class: "))
xl[6] = int(input("Input the number from where enumeration will start in 6th class: "))
xl[7] = int(input("Input the number from where enumeration will start in 7th class: "))
xl[8] = int(input("Input the number from where enumeration will start in 8th class: "))
xl[9] = int(input("Input the number from where enumeration will start in 9th class: "))


for i in range(start,end+1):
    X = plt.imread(str(i)+'.png')
    y = open(str(i)+'.txt','r')
    z = y.readlines()
    xs = X.shape[1]
    ys = X.shape[0]
    print(X.shape)
    for ent in z:
        s = ent.split(' ')
        # print(ent)
        # print(str((float(s[1])-(float(s[3])*0.5))*xs)+' to' +str(((float(s[1])+(float(s[3])*0.5))*xs)))
        # print(str((float(s[2])-(float(s[4])*0.5))*ys)+' to'+ str(((float(s[2])+(float(s[4])*0.5))*ys)))
        Y = X[int((float(s[2])-(float(s[4])*0.5))*ys):int((float(s[2])+(float(s[4])*0.5))*ys),int((float(s[1])-(float(s[3])*0.5))*xs):int((float(s[1])+(float(s[3])*0.5))*xs),:]
        print(Y.shape)
        plt.imsave(s[0]+'/'+str(xl[int(s[0])])+'.png',Y)
        xl[int(s[0])]+=1
