# https://github.com/puzzledqs/BBox-Label-Tool
from __future__ import division
from tkinter import *
import tkinter.messagebox
from PIL import Image, ImageTk
import os
import glob
import random
import pickle
import Infer
import NN
import numpy as np

# colors for the bboxes
COLORS = ['red', 'blue', 'yellow', 'pink', 'cyan', 'green', 'black']
# image sizes for the examples
SIZE = 256, 256

class LabelTool():
    def __init__(self, master):

        # set up the main frame
        self.parent = master
        self.parent.title("Street Smart")
        self.frame = Frame(self.parent)
        self.frame.pack(fill=BOTH, expand=1)
        self.parent.resizable(width = FALSE, height = FALSE)

        # initialize global state
        self.imageDir = ''
        self.imageList= []
        self.egDir = ''
        self.egList = []
        self.outDir = ''
        self.cur = 0
        self.total = 0
        self.category = 0
        self.imagename = ''
        self.labelfilename = ''
        self.tkimg = None

        # initialize mouse state
        self.STATE = {}
        self.STATE['click'] = 0
        self.STATE['x'], self.STATE['y'] = 0, 0

        # reference to bbox
        self.bboxIdList = []
        self.bboxId = None
        self.bboxList = []
        self.populationList = []
        self.typeList = []
        self.hl = None
        self.vl = None

        # ----------------- GUI stuff ---------------------
        # dir entry & load
        self.label = Label(self.frame, text = "Image Dir:")
        self.label.grid(row = 0, column = 0, sticky = E)
        self.entry = Entry(self.frame)
        self.entry.grid(row = 0, column = 1, sticky = W+E)
        self.ldBtn = Button(self.frame, text = "Load", command = self.loadDir)
        self.ldBtn.grid(row = 0, column = 2, sticky = W+E)

        # main panel for labeling
        self.mainPanel = Canvas(self.frame, cursor='tcross')
        self.mainPanel.bind("<Button-1>", self.mouseClick)
        self.mainPanel.bind("<Motion>", self.mouseMove)
        self.parent.bind("<Escape>", self.cancelBBox)  # press <Espace> to cancel current bbox
        self.parent.bind("s", self.cancelBBox)
        self.parent.bind("a", self.prevImage) # press 'a' to go backforward
        self.parent.bind("d", self.nextImage) # press 'd' to go forward
        self.mainPanel.grid(row = 1, column = 1, rowspan = 4, sticky = W+N)

        # showing bbox info & delete bbox
        self.lb1 = Label(self.frame, text = 'Bounding boxes:')
        self.lb1.grid(row = 1, column = 2,  sticky = W+N)
        self.listbox = Listbox(self.frame, width = 22, height = 12, selectmode = "multiple")
        self.listbox.grid(row = 2, column = 2, sticky = N)
        self.btnDel = Button(self.frame, text = 'Delete', command = self.delBBox)
        self.btnDel.grid(row = 3, column = 2, sticky = W+E+N)
        self.btnClear = Button(self.frame, text = 'ClearAll', command = self.clearBBox)
        self.btnClear.grid(row = 4, column = 2, sticky = W+E+N)

        # control panel for image navigation
        self.ctrPanel = Frame(self.frame)
        self.ctrPanel.grid(row = 5, column = 1, columnspan = 1, sticky = W+E)
        # self.outputBtn = Button(self.ctrPanel, text='get output', width = 10, command = self.prevImage)
        # self.outputBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.prevBtn = Button(self.ctrPanel, text='<< Prev', width = 10, command = self.prevImage)
        self.prevBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.nextBtn = Button(self.ctrPanel, text='Next >>', width = 10, command = self.nextImage)
        self.nextBtn.pack(side = LEFT, padx = 5, pady = 3)
        self.progLabel = Label(self.ctrPanel, text = "Progress:     /    ")
        self.progLabel.pack(side = LEFT, padx = 5)
        self.tmpLabel = Label(self.ctrPanel, text = "Go to Image No.")
        self.tmpLabel.pack(side = LEFT, padx = 5)
        self.idxEntry = Entry(self.ctrPanel, width = 5)
        self.idxEntry.pack(side = LEFT)
        self.goBtn = Button(self.ctrPanel, text = 'Go', command = self.gotoImage)
        self.goBtn.pack(side = LEFT)

        # example pannel for illustration
        self.egPanel = Frame(self.frame, border = 10)
        self.egPanel.grid(row = 1, column = 0, rowspan = 5, sticky = N)
        self.tmpLabel2 = Label(self.egPanel, text = "Examples:")
        self.tmpLabel2.pack(side = TOP, pady = 5)
        self.egLabels = []
        for i in range(3):
            self.egLabels.append(Label(self.egPanel))
            self.egLabels[-1].pack(side = TOP)

        # display mouse position
        self.disp = Label(self.ctrPanel, text='')
        self.disp.pack(side = RIGHT)
        self.processBtn = Button(self.ctrPanel, text = 'Process', command = self.getOutput)
        self.processBtn.pack(side = RIGHT, padx = 5, pady = 3)

        self.frame.columnconfigure(1, weight = 1)
        self.frame.rowconfigure(4, weight = 1)

        # popup menu
        self.popup_menu = Menu(self.mainPanel,tearoff = 0)

        self.popup_menu.add_command(label = 'NOTA', command = self.appendNOTA )
        self.popup_menu.add_command(label = 'BusinessAndMarketingComplexes', command = self.appendBMC)
        self.popup_menu.add_command(label = 'Residential', command = self.appendResidential)
        self.popup_menu.add_command(label = 'Offices', command = self.appendOffices)
        self.popup_menu.add_command(label = 'PowerPlants_Factories_ConstructionSites', command = self.appendPFC)
        self.popup_menu.add_command(label = 'Healthcare', command = self.appendHealth)
        self.popup_menu.add_command(label = 'Educational', command = self.appendEducational)
        self.popup_menu.add_command(label = 'GodownsAndStorage', command = self.appendGS)
        self.popup_menu.add_command(label = 'Transport', command = self.appendT)
        self.popup_menu.add_command(label = 'HotelsAndLeisure', command = self.appendHL)

    def loadDir(self, dbg = False):

        self.imageDir = self.entry.get()
        # self.imageDir = '/home/utkarsh/forboxing/1'
        self.imageList = glob.glob(os.path.join(self.imageDir, '*.jpg'))
        self.imageList = sorted(self.imageList)
        if len(self.imageList) == 0:
            print('No .JPG images found in the specified dir!')
            return

        # default to the 1st image in the collection
        self.cur = 1
        self.total = len(self.imageList)

        # set up output dir
        self.outDir = os.path.join(self.imageDir, 'output')
        if not os.path.exists(self.outDir):
            os.mkdir(self.outDir)

        filelist = glob.glob(os.path.join(self.imageDir, '*.jpg'))
        self.tmp = []
        self.egList = []
        # random.shuffle(filelist)
        for (i, f) in enumerate(filelist):
            if i == 3:
                break
            im = Image.open(f)
            r = min(SIZE[0] / im.size[0], SIZE[1] / im.size[1])
            new_size = int(r * im.size[0]), int(r * im.size[1])
            self.tmp.append(im.resize(new_size, Image.ANTIALIAS))
            self.egList.append(ImageTk.PhotoImage(self.tmp[-1]))
            self.egLabels[i].config(image = self.egList[-1], width = SIZE[0], height = SIZE[1])

        self.loadImage()
        # print ('%d images loaded' %(self.total))

    def loadImage(self):
        # load image
        imagepath = self.imageList[self.cur - 1]
        self.img = Image.open(imagepath)
        self.tkimg = ImageTk.PhotoImage(self.img)
        self.mainPanel.config(width = max(self.tkimg.width(), 400), height = max(self.tkimg.height(), 400))
        self.mainPanel.create_image(0, 0, image = self.tkimg, anchor=NW)
        self.progLabel.config(text = "%04d/%04d" %(self.cur, self.total))
        imgw = self.img.size[0]
        imgh = self.img.size[1]

        # load labels
        self.clearBBox()
        self.imagename = os.path.split(imagepath)[-1].split('.')[0]
        labelname = self.imagename + '.txt'
        self.labelfilename = os.path.join(self.outDir, labelname)
        bbox_cnt = 0
        if os.path.exists(self.labelfilename):
            with open(self.labelfilename) as f:
                content = f.readlines()
                lines = [x.strip() for x in content]
                for i in lines:
                    line = [w for w in i.split()]
                    x1 = (float(line[1]) - float(line[3])/2) * imgw
                    y1 = (float(line[2]) - float(line[4])/2) * imgh
                    x2 = (float(line[1]) + float(line[3])/2) * imgw
                    y2 = (float(line[2]) + float(line[4])/2) * imgh
                    tmp = (x1,y1,x2,y2)
                    self.bboxList.append(tuple(tmp))
                    self.typeList.append(line[5])
                    tmpId = self.mainPanel.create_rectangle(tmp[0], tmp[1], \
                                                            tmp[2], tmp[3], \
                                                            width = 2, \
                                                            outline = COLORS[(len(self.bboxList)-1) % len(COLORS)])
                    self.bboxIdList.append(tmpId)
                    self.listbox.insert(END, '(%d, %d) -> (%d, %d)' %(tmp[0], tmp[1], tmp[2], tmp[3]))
                    self.listbox.itemconfig(len(self.bboxIdList) - 1, fg = COLORS[(len(self.bboxIdList) - 1) % len(COLORS)])

    def saveImage(self):
        with open(self.labelfilename, 'w') as f:
            for i in range(len(self.bboxList)):
                box = self.bboxList[i]
                imgw = self.img.size[0]
                imgh = self.img.size[1]
                x = (box[0] + box[2]) / 2 / imgw
                y = (box[1] + box[3]) / 2 / imgh
                w = (box[2] - box[0]) / imgw
                h = (box[3] - box[1]) / imgh
                f.write("%d %f %f %f %f " % (i, x, y, w, h) + self.typeList[i] + "\n")
        # print ('Image No. %d saved' %(self.cur))

    def mouseClick(self, event):

        if self.STATE['click'] == 0 :
            self.STATE['x'], self.STATE['y'] = event.x, event.y
        else:
            try:
                self.popup_menu.tk_popup(event.x_root,event.y_root)
            finally:
                self.popup_menu.grab_release()
            x1, x2 = min(self.STATE['x'], event.x), max(self.STATE['x'], event.x)
            y1, y2 = min(self.STATE['y'], event.y), max(self.STATE['y'], event.y)
            self.bboxList.append((x1, y1, x2, y2))
            self.bboxIdList.append(self.bboxId)
            self.bboxId = None
            # https://www.tutorialspoint.com/python/tk_listbox.htm
            self.listbox.insert(END, '(%d, %d) -> (%d, %d)'%(x1, y1, x2, y2))
            self.listbox.itemconfig(len(self.bboxIdList) - 1, fg = COLORS[(len(self.bboxIdList) - 1) % len(COLORS)])
        self.STATE['click'] = 1 - self.STATE['click']

    #clear
    def mouseMove(self, event):
        self.disp.config(text = 'x: %d, y: %d' %(event.x, event.y))
        if self.tkimg:
            if self.hl:
                self.mainPanel.delete(self.hl)
            self.hl = self.mainPanel.create_line(0, event.y, self.tkimg.width(), event.y, width = 2)
            if self.vl:
                self.mainPanel.delete(self.vl)
            self.vl = self.mainPanel.create_line(event.x, 0, event.x, self.tkimg.height(), width = 2)
        if 1 == self.STATE['click']:
            if self.bboxId:
                self.mainPanel.delete(self.bboxId)
            self.bboxId = self.mainPanel.create_rectangle(self.STATE['x'], self.STATE['y'], event.x, event.y, width = 2, outline = COLORS[len(self.bboxList) % len(COLORS)])

    def cancelBBox(self, event):
        if 1 == self.STATE['click']:
            if self.bboxId:
                self.mainPanel.delete(self.bboxId)
                self.bboxId = None
                self.STATE['click'] = 0

    def delBBox(self):
        sel = self.listbox.curselection()
        if len(sel) != 1 :
            return
        idx = int(sel[0])
        self.mainPanel.delete(self.bboxIdList[idx])
        self.bboxIdList.pop(idx)
        self.bboxList.pop(idx)
        self.listbox.delete(idx)
        self.typeList.pop(idx)

    def clearBBox(self):
        for idx in range(len(self.bboxIdList)):
            self.mainPanel.delete(self.bboxIdList[idx])
        self.listbox.delete(0, len(self.bboxList))
        self.bboxIdList = []
        self.bboxList = []
        self.typeList = []

    def prevImage(self, event = None):
        self.saveImage()
        if self.cur > 1:
            self.cur -= 1
            self.loadImage()

    def nextImage(self, event = None):
        self.saveImage()
        if self.cur < self.total:
            self.cur += 1
            self.loadImage()

    def gotoImage(self):
        idx = int(self.idxEntry.get())
        if 1 <= idx and idx <= self.total:
            self.saveImage()
            self.cur = idx
            self.loadImage()

    def getOutput(self):
        L = []
        dct = {}
        dct['NOTA'] = [1,0,0,0,0,0,0,0,0,0]
        dct['BusinessAndMarketingComplexes'] = [0,1,0,0,0,0,0,0,0,0]
        dct['Residential'] = [0,0,1,0,0,0,0,0,0,0]
        dct['Offices'] = [0,0,0,1,0,0,0,0,0,0]
        dct['PowerPlants_Factories_ConstructionSites'] = [0,0,0,0,1,0,0,0,0,0]
        dct['Healthcare'] = [0,0,0,0,0,1,0,0,0,0]
        dct['Educational'] = [0,0,0,0,0,0,1,0,0,0]
        dct['GodownsAndStorage'] = [0,0,0,0,0,0,0,1,0,0]
        dct['Transport'] = [0,0,0,0,0,0,0,0,1,0]
        dct['HotelsAndLeisure'] = [0,0,0,0,0,0,0,0,0,1]
        with open('param.soc','rb') as f:
            Para = pickle.load(f)
        for i in range(len(self.bboxList)):
            box = self.bboxList[i]
            x = (box[0] + box[2]) / 2
            y = (box[1] + box[3]) / 2
            w = (box[2] - box[0])
            h = (box[3] - box[1])
            traffic, cac = NN.L_model_forward(np.expand_dims(np.array([w,h]+dct[self.typeList[i]]),axis = 0),Para)
            L.append(Infer.Rect((x,y),(w,h),float(traffic)*1000))
        Res = Infer.Infer(L,self.img.size)
        # TH = Res.TrafficMapH
        # TV = Res.TrafficMapV
        # T = Res.TrafficMap
        # with open('TrafficH.npy','rb') as f:
        #     np.save(f,TH)
        # with open('TrafficV.npy','rb') as f:
        #     np.save(f,TV)
        # with open('Traffic.npy','rb') as f:
        #     np.save(f,T)


    def appendNOTA(self):
        self.typeList.append('NOTA')

    def appendBMC(self):
        self.typeList.append('BusinessAndMarketingComplexes')

    def appendResidential(self):
        self.typeList.append('Residential')

    def appendOffices(self):
        self.typeList.append('Offices')

    def appendPFC(self):
        self.typeList.append('PowerPlants_Factories_ConstructionSites')

    def appendT(self):
        self.typeList.append('Transport')

    def appendHL(self):
        self.typeList.append('HotelsAndLeisure')

    def appendGS(self):
        self.typeList.append('GodownsAndStorage')

    def appendHealth(self):
        self.typeList.append('Healthcare')

    def appendEducational(self):
        self.typeList.append('Educational')

if __name__ == '__main__':
    root = Tk()
    tool = LabelTool(root)
    root.resizable(width =  True, height = True)
    root.mainloop()
