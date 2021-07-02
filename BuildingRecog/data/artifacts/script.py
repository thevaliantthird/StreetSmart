import os
import shutil

j = 1

for i in range(1,102):
    f = open('labels/' + str(i) + '.txt','r')
    for line in f.readlines():
        shutil.copyfile('images/'+ str(i) + '.png', 'new/images/'+ str(j) + '.png')
        with open('new/labels/'+ str(j) + '.txt','w') as g:
            g.write(line)
        j+=1
