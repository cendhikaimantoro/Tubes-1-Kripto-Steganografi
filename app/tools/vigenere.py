def encrypt(plain, raw_key):
	keyStr = raw_key
	keyAoB = bytes(keyStr, 'utf8')
	plainAoB = plain
	chiperAoB = []

	idx = 0
	for b in plainAoB:
		plainByte = b
		keyByte = keyAoB[idx%(len(keyAoB))]
		chiperByte = (plainByte+keyByte)%256
		chiperAoB.append(chiperByte)
		idx+=1

	return bytes(chiperAoB)

def decrypt(chiper, raw_key):
	keyStr = raw_key
	keyAoB = bytes(keyStr, 'utf8')
	chiperAoB = chiper
	plainAoB = []

	idx = 0
	for b in chiperAoB:
		chiperByte = b
		keyByte = keyAoB[idx%(len(keyAoB))]
		plainByte = (chiperByte+256-keyByte)%256
		plainAoB.append(plainByte)
		idx+=1

	return bytes(plainAoB)
