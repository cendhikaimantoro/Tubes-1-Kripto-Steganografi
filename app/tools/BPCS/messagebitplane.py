import math
'''
def addfile(path):
        file = open(path,"rb")
        words = bytearray(file.read())
        paddingbit = len(words)%8
        file.close()
        if paddingbit != 0:
                for i in range(0, 8-paddingbit):
                        words.append(0)
        return words


words = addfile("teks.txt")

#print(words)
#to bit stream
def tobits(string):
    result = []
    for c in string:
        bits = bin(c)[2:] 
        bits = '00000000'[len(bits):] + bits
        result.extend([int(b) for b in bits])
    return result

bitstream = tobits(words)
#print(bitstream)

def makeplanes(string):
        numofplane = math.floor(len(string)/64)
        if len(string)%64 != 0 :
                numofplane += 1
        planes = []
        
        k = 0
        for i in range(numofplane):
                plane = [[0 for i in range(8)] for i in range(8)]
                for i in range(8):
                        for j in range(8):
                                plane[i][j] = string[k]
                                k+=1
                planes.append(plane)
        return planes
'''
def byteArrToPlanes(byteArr):
    copy = bytearray(byteArr)
    remainder = len(copy)%8
    if remainder != 0:
        for i in range(8-remainder):
            copy.append(0)

    bitArr = []
    for byte in copy:
        bits = bin(byte)[2:] 
        bits = '00000000'[len(bits):] + bits
        bitArr.extend([int(b) for b in bits])  

    numofplane = len(bitArr)//64
    if len(bitArr)%64 != 0 :
            numofplane += 1
    planes = []
    
    k = 0
    for i in range(numofplane):
        plane = [[0 for i in range(8)] for j in range(8)]
        for i in range(8):
            for j in range(8):
                plane[i][j] = bitArr[k]
                k+=1
        planes.append(plane)    

    return planes
'''

print(tobits(b'lolololololololol'))
planes = makeplanes(tobits(b'lolololololololol'))

for i in planes:
    for j in i:
        print (j)
    print()


def complexity8x8(binary8x8):
	score = 0
	for i in range(8):
		for j in range(8):
			if i < 7:
				if binary8x8[i][j] != binary8x8[i+1][j]:
					score += 1
			if j < 7:
				if binary8x8[i][j] != binary8x8[i][j+1]:
					score += 1
	return score/112


def arraycomplexity(planes):
        res = []
        for i in range(len(planes)):
                res.append(complexity8x8(planes[i]))
        return res

#arraycom = arraycomplexity(planes)

def arrayconjugate(complexity, param):
        res = []
        for i in range(len(complexity)):
                if complexity[i]<param:
                        res.append(1)
                else:
                        res.append(0)
        return res

#arraycon = arrayconjugate(arraycom, 0.4)

#print(arraycon)
'''