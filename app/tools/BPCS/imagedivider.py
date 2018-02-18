import numpy as np
import cv2

def divide(img):
    height, width = img.shape[:2]
    print("%d and %d" % (width, height))
    
    x=0
    y=0
    
    if height%8!=0:
        y += 8-height%8
    if width%8!=0:
        x += 8-width%8
    
    bordered = cv2.copyMakeBorder(img, top=0, bottom=y, left=0, right=x, borderType=cv2.BORDER_CONSTANT, value=[0,0,0])
    
    height1, width1 = bordered.shape[:2]
    print("%d and %d" % (width1, height1))
    
    p = int(width/8)
    q = int(height/8)
    
    crop_img = [[0 for a in range(p)] for b in range(q)]
    for i in range(q):
        for j in range(p):
            print("%d and %d" % ((i+1)*8, (j+1)*8))
            crop_img[i][j] = bordered[i*8:(i+1)*8, j*8:(j+1)*8]
            #KALAU MAU NGETES GAMBARNYA KYK GIMANA BUKA AJA UNCOMMENT LINES DI BAWAH
            #cv2.imshow("image",crop_img[i][j])
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
            
            
            
    #crop_img berisi image 8x8
    return crop_img
    

image = cv2.imread("../../../file/input/medium_image/test.jpeg")
cropped_image = divide(image)    