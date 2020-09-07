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
from PyQt5 import QtGui, QtCore

#Setting Jet an Pink colormaps
Jetcolors = [
    (5, 5, 130),
    (0, 96, 255),
    (32, 255, 223),
    (255, 255, 0),
    (255, 64, 0),
    (128, 0, 0)
]
cmapJet = pg.ColorMap(pos=np.linspace(0.0, 1.0, 6), color=Jetcolors)
JetLUT = cmapJet.getLookupTable(alpha=False)

Pinkcolors = [
    (30, 0, 0),
    (141, 91, 91),
    (197, 138, 131),
    (219, 199, 162),
    (237, 237, 196),
    (255, 255, 255)
]
cmapPink = pg.ColorMap(pos=np.linspace(0.0, 1.0, 6), color=Pinkcolors)
PinkLUT = cmapPink.getLookupTable(alpha=False)