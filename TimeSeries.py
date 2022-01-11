# TimeSeries script
#********************************#
# S.P.P. 2019-2020  200214.1 

#   Read frames from SFile starting in-beetween STime[0] and
#   STime[0]  with step "tStep" [ms].
#   If "tStep" less than time per frame "tF" then "tStep = tF".
#   If calculated steps number greater than "maxStepNumber" 
#   then "tStep" is changed to get "maxStepNumber".
#   From each frame it extract data from rectangle

import sys
from imgUtils import Media, Cropr, printProgressBar
import numpy as np
import matplotlib.pyplot as plt

print('Running ', sys.argv[0]) #show scrypt file name

def PrintAndQuit(EStr):
    print('\n', EStr)
    input(' Press Enter')
    quit()

# default var (for stupid pylint) 
SFile = False; STime = [0]
SRect=[0, 0, 0, 0]

# # default params
tStep = 100  # time step length
maxStepNumber = 32 # maximal steps number
# subtractDark = False # subtract Dark frame singal
# #calcPreassure = False

# load external variables and parameters
scrptName = sys.argv[0].split('.')[0]
# full vars params file names are the same as scrypt name except suffix
for extnlFile in [scrptName+'_var.py', scrptName+'_prm.py']:
    try:
        with open(extnlFile, encoding='utf-8') as f:
            exec(f.read())
    except IOError:
        PrintAndQuit('IO error while exec({})'.format(extnlFile))
    print(extnlFile)    

if not SFile:
    print('SFile=',SFile) 
    PrintAndQuit('It is wrong file name'.format(SFile))
if len(STime)<2:    
    print('STime=',STime)
    PrintAndQuit('STime should have start and finish')
# создаем экземпляр чтения изображений из файла (опрделен в imUtils.py)
md = Media() 
if not md.setFile(SFile):
    PrintAndQuit('Cannot access to file ' + SFile)
md.cropr.setR_byList(SRect) # область которую будем смотреть

# направление от начала концу, положительный интервал
if STime[0]>STime[1]:
    STime[0],STime[1] = STime[1], STime[0]
deltaT = (STime[1]-STime[0])
# есть хотя бы два кадра ?
if md.fps<1 or deltaT<md.fps:
    print('\n fps={}, time inteval is {}'.format(md.fps, deltaT)) 
    PrintAndQuit('It is no suitable for video frame series') 
# шаг не меньше межкадрового интервала 
interFrame = int(1000/md.fps+1)
if interFrame > tStep: tStep = interFrame
# шагов не больше maxStepNumber
if deltaT//tStep > maxStepNumber:
    tStep = deltaT/maxStepNumber
stepNumber = int(deltaT/tStep)   
fTime = np.linspace(STime[0], STime[1], stepNumber, endpoint=True)
pVal = np.zeros_like(fTime)

for i in range(stepNumber):
    tstImg = md.freadCrop(fTime[i]) #cr.crop(md.read(fTime[i]))
    pVal[i] = tstImg.mean()
    printProgressBar(i, stepNumber-1)
    
plt.plot(fTime, pVal,'-o')
plt.title(SFile)
plt.xlabel('time [ms]')
plt.ylabel('Интенсивность')
plt.grid()
plt.show()





