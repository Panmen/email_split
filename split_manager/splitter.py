import os

MAX_SIZE = 25000000

def desplit(filename_list, dirPath):
	wholeFileData = b""
	for fileName in filename_list:
		inPath = "temporary/" + fileName
		fin = open(inPath, 'rb')
		wholeFileData += fin.read()
		fin.close
		os.remove(inPath)

	outPath = dirPath + filename_list[0][4:]
	with open(outPath, 'wb') as fout:
		fout.write(wholeFileData)
	return

def split(inPath):
    count = 0
    filename_list = []

    fileName = os.path.split(inPath)[1]

    with open(inPath, "rb") as fin:
        data = fin.read(MAX_SIZE)
        while data:
            name = "%04d%s" % (count, fileName)
            filename_list.append(name)
            outPath = os.path.join("temporary/", name)
            if not os.path.isfile(outPath):
                fout = open(outPath, 'wb')
                fout.write(data)
                fout.close
            data = fin.read(MAX_SIZE)
            count += 1
    return filename_list

