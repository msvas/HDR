import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.misc import imread, imsave

class JPGImage():
    def __init__(self, imageName, expTime):
        self.name = imageName
        self.expTime = expTime

    def readImage(self):
        image_data = imread(self.name, False, 'RGB').astype(np.float32)
        gammaExpanded = ((image_data/255)**(2.2)) * 255
        return gammaExpanded

    def processExp(self, gammaExpanded):
        redChannel = gammaExpanded[:,:,0]
        greenChannel = gammaExpanded[:,:,1]
        blueChannel = gammaExpanded[:,:,2]
        eRed = np.copy(redChannel)
        eGreen = np.copy(greenChannel)
        eBlue = np.copy(blueChannel)
        it = np.nditer(redChannel, flags=['multi_index'], op_flags=['writeonly'])
        while not it.finished:
            i = it.multi_index[0]
            j = it.multi_index[1]
            redChannel[i][j] = math.exp(curveRed[int(round(redChannel[i][j]))])
            eRed[i][j] = redChannel[i][j] / self.expTime
            greenChannel[i][j] = math.exp(curveGreen[int(round(greenChannel[i][j]))])
            eGreen[i][j] = greenChannel[i][j] / self.expTime
            blueChannel[i][j] = math.exp(curveBlue[int(round(blueChannel[i][j]))])
            eBlue[i][j] = blueChannel[i][j] / self.expTime
            gammaExpanded[i][j][0] = eRed[i][j]
            gammaExpanded[i][j][1] = eGreen[i][j]
            gammaExpanded[i][j][2] = eBlue[i][j]
            it.iternext()
        return gammaExpanded

curve = np.loadtxt('curve.txt')
curveRed = curve[:,0]
curveGreen = curve[:,1]
curveBlue = curve[:,2]

image_data1 = JPGImage("office_1.jpg", 0.0333)
gammaFixed1 = image_data1.readImage()
final1 = image_data1.processExp(gammaFixed1)

image_data2 = JPGImage("office_2.jpg", 0.1)
gammaFixed2 = image_data2.readImage()
final2 = image_data2.processExp(gammaFixed2)

image_data3 = JPGImage("office_3.jpg", 0.333)
gammaFixed3 = image_data3.readImage()
final3 = image_data3.processExp(gammaFixed3)

image_data4 = JPGImage("office_4.jpg", 0.62)
gammaFixed4 = image_data4.readImage()
final4 = image_data4.processExp(gammaFixed4)

image_data5 = JPGImage("office_5.jpg", 1.3)
gammaFixed5 = image_data5.readImage()
final5 = image_data5.processExp(gammaFixed5)

image_data6 = JPGImage("office_6.jpg", 4)
gammaFixed6 = image_data6.readImage()
final6 = image_data6.processExp(gammaFixed6)

final = (final1 + final2 + final3 + final4 + final5 + final6)/6

plt.imshow(final)
plt.show()
exit()
