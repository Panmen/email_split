from os import path

MAX_SIZE = 25000000


def split(inPath):
    count = 0
    filename_list = []

    fileName = path.split(inPath)[1]

    with open(inPath, "rb") as fin:
        data = fin.read(MAX_SIZE)
        while data:
            name = "%04d%s" % (count, fileName)
            filename_list.append(name)
            outPath = path.join("temporary/", name)
            if not path.isfile(outPath):
                fout = open(outPath, 'wb')
                fout.write(data)
                fout.close
            data = fin.read(MAX_SIZE)
            count += 1
    return filename_list

