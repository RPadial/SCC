##############################################################
#                                                            #
# Project: Design of real-time processing algorithms for     #
#          biomedical images to be implemented in the        #
#          Raspberry Pi platform                             #
# Author: Rubén Padial Allué                                 #
# mail: rubpadall@alum.us.es                                 #
# Admisor: Juan Antonio Leñero Bardallo                      #
# Date: 07-09-2020                                           #
##############################################################

import numpy as np
import pyqtgraph as pg
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import QTimer
import SCCGUI

import MyColorMaps
import SCC

import time
import numpy as np
import matplotlib.pyplot as plt
import sys

path = "/home/pi/Documents/rubpadall/SCC/Secuencia de video/"
#path = "C:/Users/Ruben/Documents/Python/SCC/Secuencia de video/"
file = np.array(["raw54.bin", "raw55.bin", "raw56.bin", "raw57.bin", "raw58.bin", "raw59.bin", "raw60.bin", "raw61.bin", "raw62.bin", "raw63.bin", 
                "raw64.bin", "raw65.bin", "raw66.bin", "raw67.bin", "raw68.bin", "raw69.bin",  "raw70.bin", "raw71.bin"])
'''
#path = "/home/pi/Documents/rubpadall/"
path = "G:/Mi unidad/Máster/TFM/07 - Imágenes/20200802/"
file = "raw69_1session.bin"
'''
##########################################################################################
#                                         DEFINES                                        #
##########################################################################################

M=80
N=60
nlevels = 10    # number of isocureves 

ColorMap = "flag"
cmap = plt.get_cmap(ColorMap)

##########################################################################################
#                                       END DEFINES                                      #
##########################################################################################

def defineGraphicsLayout():
	global win2, vb1, vb2, vb3, imv1, imv2, imv3
	pg.setConfigOptions(imageAxisOrder='row-major')	


	#GraphicsLayout (win2) with 3 ViewBox:
	# - vb1: IR image
	# - vb2: Temperature gradient
	# - vb3: Isocurves
	graphLayout = pg.GraphicsLayout()
	graphLayout.resize(900,350)

	vb1 = graphLayout.addViewBox()
	vb2 = graphLayout.addViewBox()
	vb3 = graphLayout.addViewBox()

	ui.graphicsView.setCentralItem(graphLayout)
	ui.graphicsView.resize(400,350)
	#TypeError: addItem(self, QGraphicsItem): argument 1 has unexpected type 'GraphicsLayoutWidget'

	#ImageItem imv1 addet to ViewBox vb
	vb1.setAspectLocked()
	imv1 = pg.ImageItem()
	imv1.setLookupTable(MyColorMaps.JetLUT, update=True)
	vb1.addItem(imv1)

	#ImageItem imv2 addet to ViewBox vb2
	vb2.setAspectLocked()
	imv2 = pg.ImageItem()
	imv2.setLookupTable(MyColorMaps.PinkLUT, update=True)
	vb2.addItem(imv2)

	#ImageItem imv3 addet to ViewBox vb3
	vb3.setAspectLocked()
	imv3 = pg.ImageItem()
	vb3.addItem(imv3)


def SetIsocurve(IM):
    global img, levels, curves, c, init_flag    
  
    ## generate empty curves
    curves = []
    levels = np.linspace(IM.min(), IM.max(), nlevels)

    for i in range(len(levels)):
        v = levels[i]
        # generate isocurve with cmap color selection
        pg_cmap = tuple(int(255*x) for x in cmap(i))
        pg_pen = pg.mkPen(pg_cmap)
        c = pg.IsocurveItem(level=v, pen=pg_pen)
        #c = pg.IsocurveItem(level=v, pen=(i, len(levels)*1.5))
        c.setParentItem(imv3)  # make sure isocurve is always correctly displayed over image
        curves.append(c)
    init_flag = 0

def UpdateIM():
    global IMSeg, i

    finput = path + file[i]    
    A = SCC.OpenFile(finput)
    i=i+1
    if (i==file.shape[0]-1):
    	i=0 

    IM = SCC.IM(A, N, M)
    B = SCC.SF(IM)
    IMSeg = SCC.Otsu(IM)

    imv1.setImage(IMSeg)
    imv2.setImage(B)

    #imv3.clear()
    imgLevels = (IMSeg.min(), IMSeg.max())
    imv3.setImage(IMSeg, levels=imgLevels)
    if (init_flag == 1):
        SetIsocurve(IMSeg)
    for c in curves:
        c.setData(IMSeg)

    app.processEvents()

def buttonAction():
    global IMAnalysis, TempValue, ok
    #TempValue = 0
    if ui.TempBtn.isChecked():
         ui.TempBtn.setText("Continue")
         IMAnalysis = IMSeg.copy()
         ui.AreaBtn.setEnabled(True)
         SCC.PlotIsocurve(IMAnalysis, nlevels, ShowImage='True')

    else:
         ui.TempBtn.setText("Show Temperature")
         SCC.CloseIsocurves(SCC.fig)

def AskTemperature():
    global TempValue

    TempValue = ui.tempSpin.value()
    
    tarea = time.time()
    Area = SCC.ReqArea(IMAnalysis, TempValue, "greater")
 
    ui.labelAreaValue.setText('%0.2f pixels' % Area)
    return TempValue

def ShowArea():
    global IMAnalysis, TempValue

    if ui.Showbtn.isChecked():
         ui.Showbtn.setText("Continue")

         IMAnalysis = IMSeg.copy()
         SCC.PlotRegion(IMAnalysis, ui.tempSpin.value(), ShowImage = 'True', AreaType='greater')

    else:
         ui.Showbtn.setText("Show Area")
         SCC.CloseIsocurves(SCC.figure)

def setButtonsAction(): 	
 	ui.TempBtn.clicked.connect(buttonAction)
 	ui.AreaBtn.clicked.connect(AskTemperature)
 	ui.Showbtn.clicked.connect(ShowArea)

def setTimer():
	global timer

	timer = QtCore.QTimer()
	timer.timeout.connect(UpdateIM)
	timer.start(0)
	
i = 0
init_flag = 1

if __name__ == "__main__":
	# Construc app https://doc.qt.io/qtforpython/PySide6/QtWidgets/QApplication.html
	app = QtWidgets.QApplication([]) 
	# https://doc.qt.io/qtforpython/PySide6/QtWidgets/QMainWindow.html
	ui = SCCGUI.Ui_MainWindow()
	win = QtWidgets.QMainWindow()
	win.setWindowTitle('SCC')

	#Create the widgets inside the window
	ui.setupUi(win) 				
	win.show()

	defineGraphicsLayout()
	setButtonsAction()
	setTimer()	

	sys.exit(app.exec_())

