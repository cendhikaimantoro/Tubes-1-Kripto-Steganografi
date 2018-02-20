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
	
def conjugate(binary):
	ret = []
	for i in range(len(binary)):
		ret.append([])
		for j in range(len(binary[i])):
			if (binary[i][j] == (i+j)%2):
				xor = 0
			else:
				xor = 1

			ret[i].append(xor)
	return ret