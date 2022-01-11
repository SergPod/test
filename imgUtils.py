# imgUtils
#********************************************
# (c) S.P.P. 2019-2020  200213.1
# fluorescent pressure utilities
#********************************************
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

#********************************************
#*** mask value  ***

# def mask_greater(img, maxV=254):
#     """mask too bright 2d uint8 array"""
#     if img is None: return
#     if img.dtype != 'uint8'and (maxV>255): print("WARNING!!! it is not unsigned 8-bit image")
#     return ma.masked_greater(img, maxV)


# def subAndMask(img, bgnd, minV=1):
#     """subtract dark from image and mask less then minV"""
#     if img is None: return
#     sub = img - bgnd
#     sub[sub < minV] = minV
#     return sub 


#********************************************
#*** using matpotlib present 2d array like image ***

def plot3D(a2d):
    r,c = a2d.shape
    x = np.arange(c)
    y = np.arange(r)
    x = np.meshgrid(x,y)

# show BGR image i.e. 3 colors [rows=height, columns=width, colors=3]
def plotBGR(image, title=None):
    """show BGR image using matplotlib.pyplot imshow""" 
    if (image is None): return 
    # Matplotlib expects img in RGB format but OpenCV provides it in BGR
    plt.imshow(cv.cvtColor(image, cv.COLOR_BGR2RGB))
    if title: plt.title(title)
    plt.show()


# show mono image [rows, columns]
def plotGray(image, title=None, cbar=False, cmap ='gray'):
    """show monocolor image (dim=2) as gray using matplotlib.pyplot imshow"""
    if (image is None): return 
    if (image.ndim==2):
        plt.imshow(image, cmap ) #'gray' 'Reds'
        if title: plt.title(title)
    else:    
        plt.title('Wrong image shape {}'.format(image.shape))
    if cbar: plt.colorbar()    
    plt.show() 


# show mono image [rows, columns]
def plotGray255(image, title=None, cbar=False, cmap ='gray'):
    """show monocolor image (dim=2) as gray using matplotlib.pyplot imshow"""
    if (image is None): return 
    if (image.ndim==2):
        t0 = image[0,0]; tL = image[0,-1]
        image[0,0] = 255; image[0,-1] = 0
        plt.imshow(image, cmap ) #'gray' 'Reds'
        image[0,0] = t0; image[0,-1] = tL
        if title: plt.title(title)
    else:    
        plt.title('Wrong image shape {}'.format(image.shape))
    if cbar: plt.colorbar()    
    plt.show() 


# show 2d array [rows, columns] and color bar from dark blue to yellow
def plot2dArray(array, title=None, cbar=True, cmap='viridis'):
    """show 2d array (dim=2) using matplotlib.pyplot imshow() 
    and color bar from dark blue to yellow"""
    if (array is None): return 
    if array.ndim==2: 
        plt.imshow(array, cmap)
        if title: plt.title(title)
    else:    
        plt.title('Wrong array shape {}'.format(array.shape))
    if cbar: plt.colorbar(orientation = "horizontal")    
    plt.show() 


def plotRow(image, title=None, y=0.5):
    """show monocolor image (dim=2) values along row = y*height """
    if (image is None): return 
    if (image.ndim==2):
        row = int(y*image.shape[0])
        x = range(image.shape[1])
        plt.plot(x, image[row, x] ) #'gray' 'Reds'
        plt.ylim(0., image[row,:].max()*1.1)
        plt.grid(b=True)
        if title: plt.title(title)
    else:    
        plt.title('Wrong image shape {}'.format(image.shape))
    plt.show() 


def plotRowCol(image, y=0.5, x=0.5):
    """show monocolor image (dim=2) values along row = y*height """
    if (image is None): return 
    if (image.ndim==2):
        row = int(y*image.shape[0])
        v = range(image.shape[1])
        plt.subplot(1, 2, 1)
        plt.title('Row = '+str(row))
        plt.plot(v, image[row, v] )
        col = int(x*image.shape[1])
        v = range(image.shape[0])
        plt.subplot(1, 2, 2)
        plt.title('Col = '+str(col))
        plt.plot(v, image[v, col] )
        #if title: plt.supertitle(title)
    else:    
        plt.title('Wrong image shape {}'.format(image.shape))
    plt.show() 


def plotImgs(images, titles=None, rectsize=None):
    """show image list along with titles width in rectangle with size (x,y) [inches] """
    fig = plt.figure(figsize=rectsize) #(figsize = (x.y))
    rows = (len(images)+1)//2
    for i in range(len(images)):
        if (images[i] is None):continue
        ax = fig.add_subplot(rows,2,i + 1)
        if titles: ax.set_title(titles[i])
        if images[i].ndim>2: 
            ax.imshow(cv.cvtColor(images[i], cv.COLOR_BGR2RGB))
        else: ax.imshow(images[i], 'gray')
    plt.show()


def plotImgs255(images, titles=None, rectsize=None):
    """show image list along with titles width in rectangle with size (x,y) [inches] """
    fig = plt.figure(figsize=rectsize) #(figsize = (x.y))
    rows = (len(images)+1)//2
    for i in range(len(images)):
        if (images[i] is None):continue
        ax = fig.add_subplot(rows,2,i + 1)
        if titles: ax.set_title(titles[i])
        if images[i].ndim==2:
            t0 = images[i][0,0]; tL = images[i][0,-1]
            images[i][0,0] = 255; images[i][0,-1] = 0
            ax.imshow(images[i], 'gray')
            images[i][0,0] = t0; images[i][0,-1] = tL
    plt.show()


#******************************************
#*** convert filter and transform image ***
class Imagmer:
    def __init__(self):
        self.ver = 1

    def is3Colors(self, image)->bool:
        """return True if image.ndim>2 and third dim length >2"""
        if image is None: return False
        if image.ndim < 3: return False
        if image.shape[2] < 3: return False
        else: return True   

    def bgrToRed(self, image):
        """Return Red channel of a BGR image as a monocolor image"""
        if self.is3Colors(image): return image[:,:,2]
        else: return image

    def bgrToHue(self, image):
        """Return Hue channel (0:359) of a BGR image as a monocolor image"""
        if self.is3Colors(image):

            hsv = cv.cvtColor(image, cv.COLOR_BGR2HSV)
            #h, s, v = cv.split(hsv)
            return hsv[:,:,0].astype(np.float)*2
            #return h*2
        else: return image
    

    def bgrToMonoColor(self, image, color):
        """Return Red channel of BGR image as a monocolor image"""
        if self.is3Colors(image): return image[:,:,color]
        else: return image

    def brgToGray(self, image): 
        """Return gray (brightness) image of a BGR image"""
        if self.is3Colors(image): return cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        else: return image    

    def rotate(self, image, angle, scale=1):
        if image is None: return
        if (angle==0) and (scale==1): return image 
        #1. The center with respect to which the image will rotate
        center = image.shape[1]//2, image.shape[0]//2
        #2. The angle to be rotated. In OpenCV a positive angle is counter-clockwise
        #3. Optional: A scale factor 
        size = int(image.shape[1]*scale), int(image.shape[0]*scale)
        rot_mat = cv.getRotationMatrix2D(center, angle, scale)
        return cv.warpAffine(image, rot_mat, size)

    def resize(self, image, newSize):
        """фильтр сжатия размера изображения"""
        if image is None or newSize < 4: return image
        r, c = image.shape[:2]
        oldSize = r*c
        k = np.sqrt(newSize/oldSize)
        r, c = int(k*r), int(k*c)
        if k < 1: # Preferable interpolation method cv.INTER_AREA for shrinking
            return cv.resize(image, (c,r), interpolation = cv.INTER_AREA)
        else: return image # do not increase 

    def blur(self, image, klSize, repCount=1):
        """фильтр сглаживания изображения"""
        if image is None: return
        #image = cv.medianBlur(image, 3) # median 3x3
        for i in range(repCount): # для repCount=2 делам дважды
            image = cv.GaussianBlur(image, (klSize,klSize), 0)
        return image 


#********************************************
#********** inform user  **********

def printAndQuit(EStr):
    print('\n', EStr)
    input(' Press Enter')
    quit()

def printProgressBar (iteration, total, prefix = '', suffix = '', length = 64, fill = '#', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:.0f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total+1)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


#********************************************
#********** 2D crop rectangle **********
# cr=CropR(R); cropImg=cr.crop(inImg)
#********************************************
class Cropr:
    """ cr = Cropr(yTop, yBot, xLft, xRht) or 
        cr = Cropr(); cr.setR_byList(arectList) or
        cr = Cropr(); cr.setR(yTop, yBot, xLft, xRht)    
        cropped2D=cr.crop(input2D)
    """
    def setR(self, yTop=0, yBot=2, xLft=0, xRht=2):
        if yTop > yBot: yBot, yTop = yTop, yBot
        if xLft > xRht: xLft, xRht = xRht, xLft
        self._yT = yTop
        self._yB = yBot
        self._xL = xLft
        self._xR = xRht
    
    def setR_byList(self, TBRL):
        """
        Set crop rectangle from a list variable = [yTop, yBot, xLft, xRht ..] 
        """
        if TBRL[0] > TBRL[1]: TBRL[1], TBRL[0] = TBRL[0], TBRL[1]
        if TBRL[2] > TBRL[3]: TBRL[3], TBRL[2] = TBRL[2], TBRL[3]
        self._yT = TBRL[0]
        self._yB = TBRL[1]
        self._xL = TBRL[2]
        self._xR = TBRL[3]    

    def __init__(self, yTop=0, yBot=0, xLft=0, xRht=0):  #yTop=47; yBot=153; xLft=47; xRht=253;
        #self.Cs = {'yTop':0, 'yBot':0,'xLft':0, 'xRht':0}
        #self.Cs = dict(yTop=0, yBot=0, xLft=0, xRht=10) 
        self.setR(yTop, yBot, xLft, xRht)

    def empty(self):
        """
        return true if there is not valid rectangle to crop 
        """
        r1 = (self._yT<0) or (self._xL<0) 
        r2 = (self._yB <= self._yT) or (self._xR <=self._xL)
        return r1 or r2

    def crop(self, image):
        """return image of intersection of input image rectangle and crop rectangle 
        or None if Empty intersection or no input image"""
        if image is None: return image
        if self.empty(): return None
        (r,c) = image.shape[:2]
        if (self._yT >= r) or (self._xL >= c): return None
        yB = self._yB; xR = self._xR
        if (yB >= r): yB = -1
        if (xR >= c): xR = -1
        return image[self._yT:yB, self._xL:xR]

    def cropMask(self, image):
        """return mask for intersection of input image rectangle and crop rectangle 
        or if no input image or mask of input image size if Empty crop rectangle"""
        if image is None: return image
        mask = np.ones_like(image)
        if self.empty(): return mask
 #      #
        (r,c) = image.shape[:2]
        if (self._yT >= r) or (self._xL >= c): return mask
        yB = self._yB; xR = self._xR
        if (yB >= r): yB = -1
        if (xR >= c): xR = -1
        return mask[self._yT:yB, self._xL:xR]

    def __str__(self):
        return '[{}:{}, {}:{}]'.format(self._yT, self._yB, self._xL, self._xR)


#********************************************
#********** read image from files #**********

def is_accessible(path, mode='r'):
    """
    Check if the file at 'path' can be accessed by using 'mode' open flags.
    """
    try:
        f = open(path, mode)
        f.close()
    except IOError:
        return False
    return True

# extension of popular image file types
_PIC_EXT_ = {'bmp', 'dib', 'gif', 'jpg', 'jpeg', 'png', 'webp'}

class Media:
    """
    Object to read image from video or image file and do not reopen 
    video file for the next frames if it was already used for the previous.  
    mr = Media()
    mr.setFile('v.mp4') or mr.setFile('im.png') # set used file video or image
    ret, img = mr.read(T) # seek to T ms and read frame, 
    for image file T ignored and set isPic = True
    """
    def __init__(self):
        self.vdFN = None  # video File Name
        self.imFN = None  # image File Name
        self.isPic = True # is Picture
        self.fps = 0      # frame per second
        self.cap = None
        self.cropr = Cropr()
        
    def setFile(self, FileName):
        """set file name, check if it has been set already then return True
        else check if file is accessible and return False if it is not
        else check file extention and if new file is a video then reopen 
        video cpature for it and get fps
        """    
        FileName = FileName.strip()
        if (self.vdFN==FileName) or (self.imFN==FileName):
            return True # file has been set already 
        if not is_accessible(FileName):
            #print(FileName + 'is not accessible') 
            return False    
        self.isPic = False
        p = FileName.rfind('.')
        if p:
            s = FileName[(p+1):]
            self.isPic = s in _PIC_EXT_
        if self.isPic:
            self.imFN = FileName
            self.fps = 0
        else:
            self.vdFN = FileName
            self.cap = cv.VideoCapture(FileName)
            self.fps = self.cap.get(cv.CAP_PROP_FPS) 
        return True     
            
    def read(self, Time):
        """
        Seek to T ms and read frame; for (pictures) image file Time is ignored
        return None or image
        """
        if not(self.isPic):
            if self.vdFN is None: return None
            self.cap.set(cv.CAP_PROP_POS_MSEC, Time)
            ret, img = self.cap.read()
            if ret: return img.copy()
            else: return None
        else:
            if self.imFN is None: return None
            else: return cv.imread(self.imFN)

    def freadCrop(self, Time): #
        """
        fast read video frame and return image crop created by the cropr
        """
        self.cap.set(cv.CAP_PROP_POS_MSEC, Time)
        ret, img = self.cap.read()
        if ret: return self.cropr.crop(img)

    def readFromFile(self, FileName, Time):
        """
        SetFile as FileName and read frmae at Time
        """
        if self.setFile(FileName):
            img = self.read(Time)
            return img
        else: return None

    # def readMono(self, Time, clr=2):
    #     """seek to T ms read frame and return monocolor image, if it has 
    #     BGR colors then return Red as default """
    #     if not(self.isPic):
    #         self.cap.set(cv.CAP_PROP_POS_MSEC, Time)
    #         ret, img = self.cap.read()
    #     else:
    #         img = cv.imread(self.imFN)
    #         ret = not(img is None)
    #     if ret:
    #         if isRGB(img):img = redOfBGR(img)
    #     return (ret, img)        

    # def readFirst(self, files, times):
    #     """read first frame in each file i.e. for files[i] read at times[i][0]"""
    #     imgs = []
    #     for i in range(len(files)):
    #         if files[i] is None:
    #             imgs.append(None)
    #         else:
    #             self.setFile(files[i]) # set group file to read 
    #             ret, tmp = self.read(times[i][0]) # read first image in group 
    #             if ret: imgs.append(tmp)
    #             else: imgs.append(None)            
    #     return imgs


if __name__ == "__main__":
    mF = Media()
    if not mF.setFile('data.bmp'):
        printAndQuit('Cannot access to file ' + 'data.bmp')
    img = mF.readFromFile('data.bmp', 0)
    plotBGR(img)   
    cr = Cropr(100,300,100,500)
    plotBGR(cr.crop(img))
    trm = Imagmer()
    plot2dArray(trm.brgToGray(img))




