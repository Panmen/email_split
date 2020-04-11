import os

def unsplit(filename_list, dirPath):
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
