# ImagePlot script
#********************************#
# S.P.P. 2019-2020  200214.1 

import sys
print('Running ', sys.argv[0])
# Описание скрипта ImagePlot и параметров по умолчанию

# Загрузка кадров 
#****************#
# Загружает первый кадр из DataFile. Если тербуется, 
# то также загружает кадры из DarkFile и BaseFile. 

# Обработка  кадров
#******************#
# Сглаживание кадра фильтром задается параметром
doBlur = False # если False, то не сглаживается,
# а если True, то надо указать размер ядра фильтра 
# (нечетное число) и число проходов фильтра, например  
klSize = 3; repCount=2 # ядро 3x3, применить дважды.
# Для ускорения вычислений можно уменьшить размер данных,
# необходимость уменьшения задается параметром
doResize = False 
# если False - размер остался без изменений.
# Новое количество данных в кадре задается параметром
newSize = 900 # если данных уже меньше, то ничего не 
# меняется. Сжимает cv.INTER_AREA

# Операции с кадрами
#******************#
# Если задано
subtractDark = True # тo отнимает темновой кадр из 
# остальных кадров, т.е. Data заменяется (Data-Dark) и т.д.
# Операции деления или вычитания между Base и Data задаются
BaseDivData = False # если True то результат это Base/Data
BaseSubData = False # если True и BaseDivData = False то  
# результат это (Base - Data). Если оба параметра False
# то результат просто Data и Base не грузится т.к. не требуется.

# Отображение результата
#**************************#
# Изображение графика как цветовой карты строится по 
# всем точкам результата если
setLimits = False # если True, то надо задать пределы
# например, чтобы отбразить данные со значениями от 1 до 120
minLimit = 1; maxLimit = 120
# цвета для значений определются наборами цветов, определенными
# в Matplotlib.pyplot (например 'viridis') и задаются параметром
colorMap = 'jet' # 'viridis', 'Grey 
# Значения за пределами minLimit:maxLimit показываются белым цветом.
# Дополнительно рисуется шкала цветов для данных если
colorBar = True # направление отображения шкалы задается как
barOrientation = "horizontal" # или 'vertical'

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

#Т(C) = 30 + (5/200)*Н
def calcTempre(hue):
    return 30 + hue/40

#set of functions to treat image 
def getAndTreat(fTime):
    """функция чтения и обработки изображения"""
    img = md.read(fTime) # читаем 
    if useHue:
        img = imr.bgrToHue(img) # convert and extract Hue 
        if findTempre: img = calcTempre(img)
    else:    
        if onlyRed: img = imr.bgrToRed(img) # извлекаем Redclear
        else: img = imr.brgToGray(img)
    img = imr.rotate(img, RotA) # поворот и масштабирование (scale=1)
    if DoCrop: img = cr.crop(img) # если надо обрезаем 
    if doBlur: img = imr.blur(img, klSize, repCount)  # если надо фильтруем
    if doResize: img = imr.resize(img, newSize) 
    return img
 
def subAndMask(img, bgnd, minV=1):  # отнимаем темновой
    """вычитаем и все значения < minV заменям на minV"""
    if img is None: return
    sub = img - bgnd
    mask = sub < minV
    sub[mask] = minV
    return sub 

# load Dark if needed
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

# load Base if needed and subtract Dark if needed 
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
    elif BaseSubData:
        fData = imBase - imData
else:
    fData = imData
# there is more flexible under/over range coloring see Colormap
# https://matplotlib.org/3.1.1/api/_as_gen/matplotlib.colors.Colormap.html#matplotlib.colors.Colormap
# def cLim(data, low, high):
#     dataMax=data.max()
#     dataMin=data.min()
#     sLow = dataMin + (dataMax-dataMin)*low
#     sHigh = dataMax - (dataMax-dataMin)*high
#     return [sLow, sHigh]
# if setLimits:
#     title = '{} not Full {}:{}'.format(title,partLow, partHigh)
#     partLow, partHigh = cLim(fData, partLow, partHigh)    
#     fData = ma.masked_outside(fData, partLow, partHigh)

if setLimits:
    rs = plt.imshow(fData, cmap=colorMap, vmin=minLimit, vmax=maxLimit)
    rs.cmap.set_under('black')
    rs.cmap.set_over('white')
else:
    plt.imshow(fData, cmap=colorMap)    
# if title: plt.title(title)
if colorBar:
    plt.colorbar(orientation = barOrientation)    
plt.show() 
