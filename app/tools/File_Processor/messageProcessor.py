def loadMessage(filedir):
	filenameStr = filedir.split('/')[-1]
	filenameAoB = bytes(filenameStr + '/', 'utf8')
	with open(filedir, 'rb') as f:
		data = f.read()
	data = filenameAoB + data
	return data

def parseMessage(data):
	separatorByte = bytes('/', 'utf8')
	separatorIdx=data.find(separatorByte)
	filename = data[:separatorIdx].decode('utf8')
	content = data[separatorIdx+1:]

	return filename, content
