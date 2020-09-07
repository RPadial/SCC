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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 350)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        #self.page = QtWidgets.QWidget()
        #self.page.setObjectName("page")
        
        #self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        #self.gridLayout_2.setObjectName("gridLayout_2")
        self.graphicsView = GraphicsView(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 1, 0, 1, 0)
        #self.gridLayout_2.resize(950,25)
        
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 4, 3, 1, 1)
        
        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.titleLabel.setObjectName("titleLabel")
        self.gridLayout.addWidget(self.titleLabel, 0, 0, 1, 0)

        '''
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        '''
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

        self.TempBtn = QtGui.QPushButton('Show Temperature')
        self.TempBtn.setObjectName("TempBtn")
        self.TempBtn.setCheckable(True)
        self.horizontalLayout.addWidget(self.TempBtn)

        self.AreaBtn = QtGui.QPushButton('Update Area')
        self.AreaBtn.setObjectName("AreaBtn")
        self.AreaBtn.setCheckable(False)
        self.AreaBtn.setEnabled(False)
        self.horizontalLayout.addWidget(self.AreaBtn)

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout")

        
        '''

        self.labelArea = QtWidgets.QLabel(self.centralwidget)
        self.labelArea.setObjectName("label")
        self.gridLayout.addWidget(self.labelArea, 3, 0, 1, 1)
        '''

        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.labelArea = QtWidgets.QLabel(self.centralwidget)
        self.labelArea.setObjectName("labelArea")
        self.horizontalLayout_2.addWidget(self.labelArea)
        self.labelAreaValue = QtWidgets.QLabel(self.centralwidget)
        self.labelAreaValue.setObjectName("labelAreaValue")
        self.horizontalLayout_2.addWidget(self.labelAreaValue)

        self.Showbtn = QtGui.QPushButton('Show Area')
        self.Showbtn.setObjectName("Showbtn")
        self.Showbtn.setCheckable(True)
        self.horizontalLayout_2.addWidget(self.Showbtn)

        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 0, 1, 1)

        
        MainWindow.setCentralWidget(self.centralwidget)


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