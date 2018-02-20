import numpy as np
import cv2
import math
from bitplane import isNoiseLike

class BitPlane:
    def __init__ (self, x, y, img, color, plane):
        self.x = x
        self.y = y

        self.img = img
        self.color = color
        self.plane = plane
        
    def getPlane(self):
        bit = int(math.pow(2,plane))
        plane_img = img.copy()
        plane_img.itemset((k,l,color),int(plane_img.item(k,l,color) & bit))
        return plane_img
        
    
def noiseLikeArray(img,treshold):
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
    
    p = int(width1/8)
    q = int(height1/8)
    
    crop_img = [[0 for a in range(p)] for b in range(q)]
    
    noiselike = []
    for i in range(q):
        for j in range(p):
            print("%d and %d" % ((i+1)*8, (j+1)*8))
            crop_img[i][j] = bordered[i*8:(i+1)*8, j*8:(j+1)*8]
            #KALAU MAU NGETES GAMBARNYA KYK GIMANA BUKA AJA UNCOMMENT LINES DI BAWAH
            #cv2.imshow("image",crop_img[i][j])
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
            
            
            thr = treshold #nanti ganti sama masukan user
            
            #CONTOH MANIPULASI GAMBARNYA (per pixel per warna) DI BAWAH SINI! (bikin fungsi baru aja kalau nanti ada yg mau bikin)
            for pl in range(8):
                bit = 1 << pl
                for col in range(3):
                    plane_img = crop_img[i][j].copy()
                    for k in range(8):
                        for l in range(8):
                            #crop_img.item buat ngambil nilai pixel, k,l koordinat, 0 untuk B, 1 untuk G, 2 untuk R. itemset buat set nilai pixel
                            #crop_img[i][j].itemset((k,l,0),int(crop_img[i][j].item(k,l,0)*2)%256)
                            #crop_img[i][j].itemset((k,l,1),int(crop_img[i][j].item(k,l,1)*2)%256)
                            #crop_img[i][j].itemset((k,l,2),int(crop_img[i][j].item(k,l,2)*2)%256)
                            #crop_img berisi image 8x8
                            #plane_img gambarnya udh menyesuaikan bitplane dan warnanya
                            for z in range(3):
                                if col==z:
                                    plane_img.itemset((k,l,col),int(plane_img.item(k,l,col) & bit)>>pl)
                                else:
                                    plane_img.itemset((k,l,z),0)
                    #cv2.imshow("image",plane_img)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                    plane = BitPlane(i, j, plane_img,col,pl)
                    if isNoiseLike(plane,thr):
                        noiselike.append(plane)
                        
            print("panjang array: %d" % noiselike.__len__())
    
    #cv2.imshow("image",bordered)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return bordered, noiselike
    

image = cv2.imread("../../../file/input/medium_image/test.jpeg")
cropped_image = noiseLikeArray(image, 0.3)