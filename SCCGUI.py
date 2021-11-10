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

from PyQt5 import QtCore, QtGui, QtWidgets

##########################################################################################
#                                         DEFINES                                        #
##########################################################################################
Window_x_size = 1000
Window_y_size = 350

##########################################################################################
#                                       END DEFINES                                      #
##########################################################################################

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        #See Doc/GUI.svg

        #Creates a widget with a gridLayout. https://doc.qt.io/qt-5/qmainwindow.html
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(Window_x_size, Window_y_size)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        #Creates a GraphicsView. https://doc.qt.io/qt-5/graphicsview.html to visualize the images. 
        self.graphicsView = GraphicsView(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 1, 0, 1, 0)
        #self.gridLayout_2.resize(950,25)
        
        #Add blank space in row 4 column 3 of the gridLayout
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 4, 3, 1, 1)

        #Add tittle in row 0 column 0 of the gridLayout
        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName("titleLabel")
        self.gridLayout.addWidget(self.titleLabel, 0, 0, 1, 0)

        #Creates horizontal layout 1 in row 2 column 1 of gridLayout:
        # - Position 1: labelTemp
        # - Position 2: tempSpin
        # - Position 3: labelC
        # - Position 4: TempBtn
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.labelTemp = QtWidgets.QLabel(self.centralwidget)
        self.labelTemp.setObjectName("labelTemp")
        self.horizontalLayout.addWidget(self.labelTemp)
 
        self.tempSpin = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.tempSpin.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.tempSpin.setProperty("value", 36)
        self.tempSpin.setObjectName("tempSpin")
        self.horizontalLayout.addWidget(self.tempSpin)
 
        self.labelC = QtWidgets.QLabel(self.centralwidget)
        self.labelC.setObjectName("label")
        self.horizontalLayout.addWidget(self.labelC)

        self.TempBtn = QtWidgets.QPushButton('Show Temperature')
        self.TempBtn.setObjectName("TempBtn")
        self.TempBtn.setCheckable(True)
        self.horizontalLayout.addWidget(self.TempBtn)

        self.AreaBtn = QtWidgets.QPushButton('Update Area')
        self.AreaBtn.setObjectName("AreaBtn")
        self.AreaBtn.setCheckable(False)
        self.AreaBtn.setEnabled(False)
        self.horizontalLayout.addWidget(self.AreaBtn)

        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        #Creates horizontal layout 2 in row 3 column 1 of gridLayout:
        # - Position 1: labelArea
        # - Position 2: labelAreaValue
        # - Position 3: Showbtn
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout")        

        self.labelArea = QtWidgets.QLabel(self.centralwidget)
        self.labelArea.setObjectName("labelArea")
        self.horizontalLayout_2.addWidget(self.labelArea)

        self.labelAreaValue = QtWidgets.QLabel(self.centralwidget)
        self.labelAreaValue.setObjectName("labelAreaValue")
        self.horizontalLayout_2.addWidget(self.labelAreaValue)

        self.Showbtn = QtWidgets.QPushButton('Show Area')
        self.Showbtn.setObjectName("Showbtn")
        self.Showbtn.setCheckable(True)
        self.horizontalLayout_2.addWidget(self.Showbtn)

        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 0, 1, 1)

        #Set QWidget centralwidget as central widget of MainWindow
        MainWindow.setCentralWidget(self.centralwidget)

        #Set text values
        self.retranslateUi(MainWindow)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SCC"))
        self.titleLabel.setText(_translate("MainWindow", "SCC"))
        self.labelTemp.setText(_translate("MainWindow", "Temperature:"))
        self.labelC.setText(_translate("MainWindow", "ºC"))
        self.labelArea.setText(_translate("MainWindow", "Area:"))
        self.labelAreaValue.setText(_translate("MainWindow", "0"))

from pyqtgraph import GradientWidget, GraphicsView, SpinBox
#from pyqtgraph.widgets.RawImageWidget import RawImageWidget