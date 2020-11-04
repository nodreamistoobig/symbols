import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from skimage.filters import threshold_otsu, try_all_threshold, threshold_triangle
from scipy.ndimage import morphology


def lakes(image):
    B = ~image
    BB = np.ones((B.shape[0]+2, B.shape[1]+2))
    BB[1:-1, 1:-1] = B
    return np.max(label(BB)) - 1

def has_vline(image):
    lines = np.sum(image, 0) // image.shape[0]
    return 1 in lines

def has_bay(image):
    b = ~image
    bb = np.zeros((b.shape[0] + 1, b.shape[1])).astype("uint8")
    bb[:-1, :] = b
    return lakes(~bb)-1

def count_bays(image):
    holes = ~image.copy()
    return np.max(label(holes))
    
def recognize(region):
    lc = lakes(region.image)
    bays = count_bays(region.image)
    #print(lc, bays)
    if lc == 2:
        if has_vline(region.image):
            return "B"
        return "8"
    if lc == 1:
        if has_bay(region.image) > 0:
            return "A"
        else:
            if bays<5:
                if (region.perimeter**2 / region.area) > 50:
                    return "D"
                else:
                    return "P"
        return "0"
    if lc == 0:
        if has_vline(region.image):
            if np.all(image == 1):
                return "-"
            return "1"
        
        if bays == 2:
            return "/"
        
        if bays > 3:
            # print(region.area/ (region.image.shape[0]*region.image.shape[1]))
            if (region.perimeter**2 / region.area) > 70:
                return "*"   
            if bays == 5:
                return "W"
            if bays == 4:
                return "X"


    return "None"
    

image = plt.imread("symbols.png")
#image = plt.imread("alphabet.png")
image = np.sum(image, 2)
image[image > 0] = 1

labeled = label(image)            
print(np.max(labeled))

regions = regionprops(labeled)

d = {}
i=1
for region in regions:
    symbol = recognize(region)
    if (symbol == 'None'):
        print(i)
    if symbol not in d:
        d[symbol] = 1
    else:
        d[symbol] += 1
    i+=1
        

        
print(d)

plt.figure()
plt.subplot(121)

plt.imshow(~regions[1].image)
plt.subplot(122)
plt.imshow(labeled)
plt.show()
