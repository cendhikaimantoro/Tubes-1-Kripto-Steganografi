import random
import math
import cv2
from .complexity import complexity8x8, conjugate
from .imageprocessor import noiseLikeArray
from .messagebitplane import byteArrToPlanes


def insertplane(img, plane, data):
	copy = img
	for i in range(8):
		for j in range(8):
			imgX = (plane.x)*8+i
			imgY = (plane.y)*8+j
			rgb = plane.color
			if data [i][j] == 0:
				mask = ~(1<<plane.plane)
				copy.itemset((imgX, imgY, rgb), int(copy.item(imgX,imgY,rgb))&mask )
			elif data[i][j] == 1:
				mask = 1<<plane.plane
				copy.itemset((imgX, imgY, rgb), int(copy.item(imgX,imgY,rgb))|mask)

	return copy


def getData8x8(img, plane):
	ret = []
	for i in range(8):
		ret.append([])
		for j in range(8):
			imgX = (plane.x)*8+i
			imgY = (plane.y)*8+j
			rgb = plane.color
			byte = img.item(imgX,imgY,rgb)
			bit = (byte>>(plane.plane ))&1
			ret[i].append(bit)
	return ret


def intToBit8x8(x):
	bit64 = []
	for i in range(64):
		bit64.append(0)
	idx = -1
	while x > 0:
		bit64[idx] = x%2
		x = x//2
		idx -= 1

	bit8x8 = []
	for i in range(64):
		if (i%8 == 0):
			bit8x8.append([])
		bit8x8[i//8].append(bit64[i])

	return bit8x8

def bit8x8ToInt(d):
	x = 0
	for i in range(64):
		x *= 2
		x += d[i//8][i%8]
	return x

def insertMessage(imagedir, messageAoB, key, treshold):
	#Disini processing pesan sampai dapat ordered array of non-informative-data
	dataPlane = byteArrToPlanes(messageAoB)


	#Disini processing plane sampai dapat ordered array of non-informative-plane
	img = cv2.imread(imagedir)
	fullimage, nonInformativePlane = noiseLikeArray(img, treshold)
	bordered = fullimage.copy()
	nonInformativePlane2 = nonInformativePlane #

	#counting payload and allocating bitplane
	sizeBitPlane = len(nonInformativePlane)
	allocation = []
	allocation.append(sizeBitPlane)
	while(allocation[-1] > 1):
		allocation.append((allocation[-1]+63)//64)
	nReservedPlane = 1  #1 for storing data length
	for n in allocation[1:]:
		nReservedPlane += n
	allocation[0] -= nReservedPlane
	sizeDataPlane = allocation[0]
	print(len(nonInformativePlane))
	payload = sizeDataPlane*8

	dataSize = len(dataPlane)

	if len(messageAoB) <= payload:
		allocation[0] = len(dataPlane)
		
		rawDataPlane= dataPlane
		nonInformativeDataPlane = []
		for level in range(len(allocation)):
			if level < len(allocation)-1:
				conjugationDataPlane = []
				temporaryDataPlane = []
				for i in range(allocation[level+1]):
					conjugationDataPlane.append([])
					for j in range(8):
						conjugationDataPlane[i].append([])
						for k in range(8):
							idx = 64*i + 8*j +k
							if idx in range(len(rawDataPlane)):
								plane = rawDataPlane[idx]
								if complexity8x8(plane) > treshold:
									temporaryDataPlane.append(plane)
									conjugationDataPlane[i][j].append(0)
								else:
									plane = conjugate(plane)
									temporaryDataPlane.append(plane)
									conjugationDataPlane[i][j].append(1)
							else:
								conjugationDataPlane[i][j].append(random.randrange(2))
				nonInformativeDataPlane = temporaryDataPlane + nonInformativeDataPlane
				rawDataPlane = conjugationDataPlane
			else:
				#rootplane
				isRootConjugated = 0
				plane = rawDataPlane[0]
				temporaryDataPlane = []
				if complexity8x8(plane) > treshold:
					temporaryDataPlane.append(plane)
					isRootConjugated = 0
				else:
					plane = conjugate(plane)
					temporaryDataPlane.append(plane)
					isRootConjugated = 1
					
				nonInformativeDataPlane = temporaryDataPlane + nonInformativeDataPlane

				#lengthplane
				plane = [[0 for i in range(8)] for i in range(8)]

				length = len(messageAoB)

				arr = []
				for i in range(64):
					arr.append(length>>(63-i)&1)
				plane = []
				for i in range(8):
					plane.append([])
					for j in range(8):
						plane[i].append(arr[8*i+j])

				plane[0][0] = isRootConjugated
				lengthPlane = plane #

				nonInformativeDataPlane = [conjugate(plane)] + nonInformativeDataPlane


		shuffledOrder = [i for i in range(sizeBitPlane)]
		random.seed(key)
		random.shuffle(shuffledOrder)

		bitPlane1 = '' #
		for i in range(len(nonInformativeDataPlane)):	
			fullimage = insertplane(fullimage, nonInformativePlane[shuffledOrder[i]], nonInformativeDataPlane[i])
			if i == 0:
				bitPlane1 = nonInformativePlane[shuffledOrder[i]]
		status = 1
		payload = payload
		messagesize = len(messageAoB)
		image = fullimage

		return status, payload, messagesize, image

	else:				
		status = 0
		payload = payload
		messagesize = len(messageAoB)
		image = img
		print(len(noiseLikeArray(image, treshold)[1]))
		return status, payload, messagesize, image

			
#########################################################################################################################
def extractMessage(imgdir, key, treshold):
		steganoimage = cv2.imread(imgdir)
		steganoImage, nonInformativePlane = noiseLikeArray(steganoimage, treshold)
		sizeBitPlane = len(nonInformativePlane)
		print(len(nonInformativePlane))

		allocation = []
		allocation.append(sizeBitPlane)
		while(allocation[-1] > 1):
			allocation.append((allocation[-1]+63)//64)
		nReservedPlane = 1  #1 for storing data length
		for n in allocation[1:]:
			nReservedPlane += n
		allocation[0] -= nReservedPlane

		shuffledOrder = [i for i in range(sizeBitPlane)]
		random.seed(key)
		random.shuffle(shuffledOrder)

		lengthPlane2 = conjugate(getData8x8(steganoimage, (nonInformativePlane[shuffledOrder[0]])))

		isRootConjugated = lengthPlane2[0][0]
		lengthPlane2[0][0] = 0
		length = bit8x8ToInt(lengthPlane2)
		print(lengthPlane2)

		allocation[0] = (length+7)//8


		dataPlane = []
		for i in range(nReservedPlane+allocation[0]):
			dataPlane.append(getData8x8(steganoimage,nonInformativePlane[shuffledOrder[i]]))

		outputBitPlane = lengthPlane2
		outputBitPlane[0][0] = isRootConjugated
		outputBitPlane = [outputBitPlane]
		remainder = dataPlane[1:]
		for i in reversed(range(len(allocation))):
			conjugationBitPlane = outputBitPlane
			outputBitPlane = remainder[:allocation[i]]
			for j in range(len(outputBitPlane)):
				if conjugationBitPlane[j//64][j%64//8][j%8] == 1:
					outputBitPlane[j] = conjugate(outputBitPlane[j])
			remainder = remainder[allocation[i]:]


		bufferByte = outputBitPlane
		byteArr = []
		for i in range(length):
			byte = bufferByte[i//8][i%8]
			sum = 0
			for j in range(8):
				sum*=2
				sum+=byte[j]
			byteArr.append(sum)
		byteArr = bytearray(byteArr)

		return byteArr

def psnr(imgdir1, imgdir2):
	img1 = cv2.imread(imgdir1)
	img2 = cv2.imread(imgdir2)
	height1, width1 = img1.shape[:2]
	height2, width2 = img2.shape[:2]

	M = min(width1, width2)
	N = min(height1,height2)

	rms = 0

	for i in range(M):
		for j in range (N):
			for k in range(3):
				val1 = img1.item(i,j,k)
				val2 = img2.item(i,j,k)
				rms += (val1-val2)*(val1-val2)
	rms = math.sqrt(rms/M/N/3)

	ret = 20 * math.log10(256/rms)
	return ret




	
