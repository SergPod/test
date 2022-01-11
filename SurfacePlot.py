# SurfacePlot script
#********************************#
#  S.P.P. 2019-2020  200414.1 

import sys
print('Running ', sys.argv[0])
# Описание скрипта SurFacePlot и параметров по умолчанию

# Загрузка кадров 
#****************#
# Загружает первый кадр из DataFile. Если тербуется, то 
# также загружает кадры из DarkFile и BaseFile. 

# Обработка  кадров
#******************#
# Сглаживание кадра фильтром задается параметром
doBlur = False # если False, то не сглаживается,
# а если True, то надо указать размер ядра фильтра 
# (нечетное число) и число проходов фильтра, например  
klSize = 3; repCount=2 # ядро 3x3, применить дважды.
# Для ускорения вычислений и быстрой манипуляцией 3D
# поверхнеостью желательно уменьшить размер данных
# необходимость уменьшения задается параметром
doResize = True # если False - размер останется без изменений 
# новое количество данных в кадре задается параметром
newSize = 1200 # если данных уже меньше ничего не меняется

# Операции с кадрами
#******************#
# Если задано
subtractDark = True # тo отнимает темновой кадр из 
# остальных кадров, т.е. Data заменяется (Data-Dark) и т.д.
# Операции деления или вычитания между Base и Data задаются
BaseDivData = False # если True то результат это Base/Data
BaseSubData = False # если True и BaseDivData = False то  
# результат это (Base - Data). Если оба параметра False
# то результат просто Data. Base не грузится т.к. не требуется.

# Отображение результата
#**************************#
# нет параметров


import cv2 as cv
import numpy as np; import numpy.ma as ma
import matplotlib.pyplot as plt
from imgUtils import Media, Cropr, Imagmer, printAndQuit# and auxiliary

#calcPreassure = False

# load external variables and parameters
scrptName = sys.argv[0].split('.')[0]
# full vars file & params file names are the same as scrypt name except suffix
for extnlFile in [scrptName+'_var.py', scrptName+'_prm.py']:
    try:
        with open(extnlFile, encoding='utf-8') as f:
            exec(f.read())
    except IOError:
        printAndQuit('IO error while exec({})'.format(extnlFile))
    print(extnlFile)    

# check that vars have provided required files names
needBaseFile = bool(BaseDivData or BaseSubData)
if not(DataFile): 
    printAndQuit('There is no Data frame file name! Press Enter')
if subtractDark and not(DarkFile): 
    printAndQuit('There is no Dark frame file name! Press Enter')
if needBaseFile and not(BaseFile): 
    printAndQuit('There is no Off wind frame file name! Press Enter')

imr = Imagmer()
md = Media() # создаем экземпляр чтения изображений из файла (опрделен в imUtils.py)
if DoCrop:   # create cr to crop rectangle (defined in imUtils.py)
    cr = Cropr()
    cr.setR_byList(CropRect)


# check that DataFile is accessible
if not md.setFile(DataFile):
    printAndQuit('Cannot access to file ' + DataFile)

#set of functions to treat image 
def getAndTreat(fTime):
    """функция чтения и обработки изображения"""
    img = md.read(fTime) # читаем 
    if useHue:
        img = imr.bgrToHue(img) # convert and extract Hue
    else:     
        if onlyRed: img = imr.bgrToRed(img) # извлекаем
        else: img = imr.brgToGray(img)
    img = imr.rotate(img, RotA) # поворот и масштабирование (scale=1)
    if DoCrop: img = cr.crop(img) # если надо обрезаем 
    if doBlur: img = imr.blur(img)  # если надо фильтруем
    if doResize: img = imr.resize(img, newSize) 
    return img
 
def subAndMask(img, bgnd, minV=1):  # отнимаем темновой
    """вычитаем и все значения < minV заменям на minV"""
    if img is None: return
    sub = img - bgnd
    mask = sub < minV
    sub[mask] = minV
    return sub 

# load Dark if it is needed
if subtractDark:
    if not md.setFile(DarkFile):
        printAndQuit('Cannot access to file ' + DarkFile)
    imDark = getAndTreat(DarkTime[0]).astype(np.int16) 
    print('Dark', DarkFile, DarkTime[0])

# load Data and subtract Dark if needed
if not md.setFile(DataFile):  
    printAndQuit('Cannot access to file ' + DataFile)
imData = getAndTreat(DataTime[0]).astype(np.int16)#byte to 16bit for substraction
print('Data', DataFile, DataTime[0])
if subtractDark:
    imData =imData - imDark

# load Base if need for it and subtract Dark if it is required
if needBaseFile:
    if not md.setFile(BaseFile):
        input('Cannor access to file ' + BaseFile)
        
        quit()
    imBase = getAndTreat(BaseTime[0]).astype(np.int16)
    print('Off wind', BaseFile, BaseTime[0])
    if subtractDark:
        imBase = imBase - imData
    if BaseDivData:
        imData[imData<1] = 1
        fData = imBase/imData
        title = 'Base/Data'
    elif BaseSubData:
        fData = imBase - imData
        title = 'Base-Data'
else:
    fData = imData
    title = 'Temperature, K'

print('Frames have been Loaded & treated')

def plot3d(a2d):
    r,c = a2d.shape
    x = np.array(range(c))
    y = np.array(range(r)) 
    X, Y = np.meshgrid(x,y)
    if useHue and findTempre:
        a2d = a2d/40 + 30 + 273
    #if stDebug: print(X.shape,'  Y', Y.shape,'  Z', a2d.shape)
    # Plot the surface.
    fig = plt.figure()# figsize = (10,8))
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X, Y, a2d, cmap='winter',
                       linewidth=0, antialiased=False)    
    # fig = plt.figure() #(figsize = (10,8))
    # ax = plt.axes(projection="3d")
    # if findTempre:
    #     ax.plot_surface(X, Y, a2d, rstride=.1, cstride=.1, cmap='winter', edgecolor='none')  #  
    # else:
    #     ax.plot_surface(X, Y, a2d, rstride=1, cstride=1, cmap='winter', edgecolor='none')  # rstride=1, cstride=1,     
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('T ')#, fontsize='large')
    plt.title(title)
    plt.show()
    #plt.savefig("Pxps.png")

levelCount = 7

def levels(a2d):
    r,c = a2d.shape
    x = np.array(range(c))
    y = np.array(range(r))
    X, Y = np.meshgrid(x,y)
    #if stDebug: print(X.shape,'  Y', Y.shape,'  Z', a2d.shape)
    fig = plt.figure() #(figsize = (10,8))
    left, bottom, width, height = 0.1, 0.1, 0.8, 0.8
    ax = fig.add_axes([left, bottom, width, height]) 
    #cp = ax.contourf(X, Y, a2d, levelCount)
    #or
    cp = ax.contour(X, Y, a2d, levelCount)
    ax.clabel(cp, inline=True, 
            fontsize=10)
    ax.set_title('Contour Plot')
    ax.set_xlabel('x (mm)')
    ax.set_ylabel('y (mm)')
    plt.show()
    #plt.savefig("Pxpc.png")

print('Creating plot...')
plot3d(fData)
# levels(fData)