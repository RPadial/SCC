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

import struct
import numpy as np
import math
import scipy 
import matplotlib.pyplot as plt

from skimage import data
from skimage import filters
from skimage import exposure
from skimage import measure


K = np.array([  [47, 0, -47],
                [162, 0, -162], 
                [47, 0, -47]
            ])  # Sobel-Feldman operator
            
'''


K = np.array([  [-47, 0, 47],
                [-162, 0, 162], 
                [-47, 0, 47]
            ])  # Sobel-Feldman operator
'''
'''
K = np.array([[ -3-3j, 0-10j,  +3 -3j],
                   [-10+0j, 0+ 0j, +10 +0j],
                    [ -3+3j, 0+10j,  +3 +3j]]) # Gx + j*Gy

'''
u = np.array([1, 2, 1])

'''
T2=36.8
T1=36.6

R1=8250
R2=8300

'''
T2=37.1;
T1=36.0;

R1=8250;
R2=8400;

M=80
N=60
###################################################################################

def OpenFile(finput):
    # Open 'finput' .bin file packaged and return a list 'L'. Data packaged is unsigned-sorts little-endian
    #reading unsigned shorts 'tuple'??
    with open(finput, "rb") as fid:
        #Max = struct.unpack('H', fid.read(2))         # <little-endian
        L = list(struct.iter_unpack('<H', fid.read()))
        L = np.asarray(L)                              # tuple to array
        L = np.reshape(L,L.shape[0],'C')
    return L


def List2Im(L, N=N, M=M, f=3):
    # L: List of data
    # N: number of rows
    # M: number of columns
    # f: first data component of the image. 
    #Word 1: Minimum value of the scene
    #Word 2: Maximum value of the scene
    #The rest are 80x60 unsigned shorts, listed by row then column
    k=f-1

    IM = np.zeros((N,M))

    for i in range(0,N):
        IM[i,:]=L[k+i*M:i*M+M+k]

    return IM


def GetImage(finput, N=N, M=M, f=3):
    # Return a Image as a matrix MxN from finput
    IM = List2Im(OpenFile(finput), N, M, f)
    return IM


def GetImage2(finput):
    A = OpenFile(finput)
    Max = A[0]
    Min = A[1]
    k=3-1

    IM = np.zeros((N,M))

    for i in range(0,N):
        for j in range(0,M):
            IM[i,j]=A[k]
            k=k+1

    '''
    for i in range(0,N):
        IM[i,:]=A[k+i*M:i*M+M+k]
    '''
    return IM
    

def IM (A, N=N, M=M, f=3):
    
    IM = List2Im(A, N, M, f)    
            
    #Now we use the the measured temperature in two body spots to callibrate the sensor
    a=(T2-T1)/(R2-R1)
    b=T2-a*R2

    IM=IM*a+b


    #MinVal = math.floor(np.amin(IM))
    #MaxVal = math.ceil(np.amax(IM))
    return IM

def IM2 (A, M=M, N=N):
    
    Max = A[0]
    Min = A[1]
    k=3-1

    IM = np.zeros((N,M))

    for i in range(0,N):
        for j in range(0,M):
            IM[i,j]=A[k]
            k=k+1
            
    #Now we use the the measured temperature in two body spots to callibrate the sensor
    a=(T2-T1)/(R2-R1)
    b=T2-a*R2

    IM=IM*a+b

    MinVal = math.floor(np.amin(IM))
    MaxVal = math.ceil(np.amax(IM))
    return IM

def Im2Ter (IM, T1=T1, T2=T2, R1=R1, R2=R2):
    
    # Transform image IM pixel values to temperature values in ºC

    N = IM.shape[0]  # number of rows
    M = IM.shape[1]  # number of columns
    TerIM = np.zeros((N,M))
    #Now we use the the measured temperature in two body spots to callibrate the sensor
    a=(T2-T1)/(R2-R1)
    b=T2-a*R2

    TerIM=IM*a+b

    #MinVal = math.floor(np.amin(IM))
    #MaxVal = math.ceil(np.amax(IM))
    return TerIM

def SF(TerIM, Kernel=K):

    MK = K.shape[0]  # number of rows
    NK = K.shape[1]  # number of columns

    M = TerIM.shape[0]  # number of rows
    N = TerIM.shape[1]  # number of columns
    
    G = np.zeros((M,N))
    
    #G = scipy.signal.convolve2d(TerIM, Kernel, mode='same', boundary='fill', fillvalue=0)
    G = scipy.signal.convolve2d(TerIM, np.flip(Kernel), boundary='symm', mode='same')
    '''
    for i in range(MK-2,M-MK+1):
        for j in range (NK-2,N-NK+1):
            #B[i,j]=np.sum(np.sum(K*A(range(i-((MK-1)//2),i+((MK-1)//2)),range(j-((NK-1)//2),j+((NK-1)//2)))))
            G[i,j]=np.sum(K*TerIM[i-((MK-1)//2):i+((MK-1)//2)+1,j-((NK-1)//2):j+((NK-1)//2)+1])
    
    '''
    # MinTemp = np.min(A)
    # MaxTemp = np.max(A)

    # MaxVar=MaxTemp-MinTemp

    MinVal = math.floor(np.min(G))
    MaxVal = math.ceil(np.max(G))

    M = G.shape[0]  # number of rows
    N = G.shape[1]  # number of columns
    #t = time.time()
    
    for i in range(0, M):
        for j in range(0, N):
        
            if G[i,j]>0:
                G[i,j]=G[i,j]/MaxVal#*(MaxVar/MaxVal)
            else:
                G[i,j]=-G[i,j]/MinVal#*(MaxVar/MinVal)

    return G

def sobelkernel(size, varargin=[]):
    #SOBELKERNEL returns sobel kernel
    #   KERNEL=SOBELKERNEL(SIZE) Returns Sobel filter of predefined size.
    #
    #   KERNEL=SOBELKERNEL(SIZE, 'NORMALISED') The Sobel matrix should be
    #   normalised if proper derivative estimator is required.
    #
    #   [KERNEL, S, D]=SOBELKERNEL(SIZE, 'NORMALISED') Returns also smoothing S
    #   and derivative D components individually. The kernel is then a
    #   multiplication of these two vectors: S'*D. This can be usefull for
    #   convolution acceleration via separable kernels as illustrated at:
    #       http://blogs.mathworks.com/steve/2006/10/04/separable-convolution/
    #   
    #   Example
    #   -------
    #       sobelkernel(4)
    #
    #   See also IMFILTER, FSPECIAL.
    #   Contributed by Jan Motl (jan@motl.us)
    #   $Revision: 1.1 $  $Date: 2013/02/13 16:58:01 $
    #   For method description see:
    #       http://stackoverflow.com/questions/9567882/sobel-filter-kernel-of-large-size
    # Parameter checking.


    # Parameter checking.
    if (len(varargin)!=0) and (varargin == 'normalise'):
        normalisation = 1/8
    else:
        normalisation = 1
    
    # The dafault 3x3 Sobel kernel.
    s = normalisation * u;
    d = np.array([1, 0, -1])

    # Convolve the default 3x3 kernel to the desired size.
    for i in range(0, size-3):
        s = normalisation * np.convolve(u, s,)
        d = np.convolve(u, d)
    #kernel = np.dot(x,d);
    
    kernel = np.zeros((s.shape[0],d.shape[0]))

    for i in range(0, s.shape[0]):
        for j in range(0, d.shape[0]):
            kernel[i,j]=s[i]*d[j]
    
    return kernel

def Otsu (IM, thr="lower"):
    
    val = filters.threshold_otsu(IM)
    #hist, bins_center = exposure.histogram(IM)
    N = IM.shape[0]  # number of rows
    M = IM.shape[1]  # number of columns
    
    #IMOtsu = IM
    IMOtsu = IM.copy()
    MinVal = math.floor(np.amin(IM))
    MaxVal = math.ceil(np.amax(IM))
    
    if (thr == "lower"):
        
        for i in range(0,N):
            for j in range(0,M):
                if (IMOtsu[i,j]<val):
                    IMOtsu[i,j]=MinVal
    elif(thr == "upper"):
        for i in range(0,N):
            for j in range(0,M):
                if (IMOtsu[i,j]>val):
                    IMOtsu[i,j]=MinVal
                    
                    
    return IMOtsu
    
'''
def StartIsocurve(x, y, Tittle, ColorMap):
    #global app, win2, vb
    cmap = plt.get_cmap(ColorMap)
    ## Always start by initializing Qt (only once per application)
    app = pg.mkQApp()
    #win = QtGui.QMainWindow()
    # container widget with a layout to add QWidgets to

    # win.show()
    ####
    win2 = pg.GraphicsWindow()
    win2.setWindowTitle(Tittle)
    vb = win2.addViewBox()
    win2.resize(x,y)
    return vb'''


def CoordinateMethods(xi, yi):
    #xi: array with x coordinates of a isocurve
    #yi: array with y coordinates of a isocurve
    S1 = xi[1]*yi[1+1]
    S2 = xi[1+1]*yi[1]
    for i in range (0, xi.shape[0]-1):
        S1 = S1 + xi[i]*yi[i+1]
        S2 = S2 + xi[i+1]*yi[i]

    Area = abs(S1-S2)/2

    return Area

def SiftingArea(Arrays):
    size_Arrays = np.shape(Arrays)
    #print('shape = ', size_Arrays[0])
    n_Arrays = np.zeros(size_Arrays[0])

    for i in range(size_Arrays[0]):
        Array_x = Arrays[i]
        n_Arrays [i] = Array_x.shape[0]
        
    max_index = np.where(n_Arrays==(np.max(n_Arrays)))
    max_index = (np.asarray(max_index[0]))
    np.reshape(max_index,max_index.shape[0],'C')
    return int(max_index)

def ReqArea(IM, level, AreaType='sum'):
    Area = 0
    if (level < np.amin(IM) or level > np.amax(IM)):
        return 0
    else:
        ContourCordinates = measure.find_contours(IM, level) #Retunrs (row, column) array
        #↨ContourCordinates = ContourCordinates[(SiftingArea(ContourCordinates))]
        size_contour = np.shape(ContourCordinates)
        CC = np.zeros(size_contour[0])

        if (AreaType == "sum"):
            for i in range(size_contour[0]):
                A = ContourCordinates[i]

                Area = Area + CoordinateMethods(A[:,1], A[:,0])    # xi = column, yi =row
        elif (AreaType == "greater"):
            SiftingArea(ContourCordinates)
            A = ContourCordinates[SiftingArea(ContourCordinates)]
            Area = CoordinateMethods(A[:,1], A[:,0])

        
        return Area

def  PlotIsocurve(IM, nlevels, ShowImage = 'False'):
    global fig

    fig = plt.figure("Isoterm")
    ax = fig.add_subplot(111)


    if ShowImage == 'True':
        ax.imshow(IM, cmap='Greys')

    cont = plt.subplot()
    cs = cont.contour(IM, nlevels, origin='lower')
    ax.clabel(cs)

    plt.show()

def CloseIsocurves(Fig):
    
    plt.close(Fig)

def PlotRegion(IM, level, ShowImage = 'False', AreaType='sum'):
    global figure
    contours = measure.find_contours(IM, level)
    # Display the image and plot all contours found
    figure, ax = plt.subplots()
    if ShowImage == 'True':
        ax.imshow(IM, cmap=plt.cm.gray)


    if (AreaType=="sum"):
        for n, contour in enumerate(contours):
            ax.plot(contour[:, 1], contour[:, 0], linewidth=2)
    elif (AreaType=="greater"):
        contours = contours[(SiftingArea(contours))]
        ax.plot(contours[:, 1], contours[:, 0], linewidth=2)

    

    ax.axis('image')
    ax.set_xticks([])
    ax.set_yticks([])
    plt.show()
