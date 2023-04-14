sbox1 = ['101', '010', '001', '110', '011', '100', '111', '000', '001', '100', '110', '010', '000', '111', '101', '011']
sbox2 = ['100', '000', '110', '101', '111', '001', '011', '010', '101', '011', '000', '111', '110', '010', '001', '100']
rounds = 8
permutation = [0,1,3,2,3,2,4,5]
key = '10101010'


def prepareImage():
    with open('./img2.pbm', "rb") as image:
        imageBytesArray = []
        lines = image.readlines()

        imageBytes = lines[3:]
        for line in imageBytes:
            line = str(line)
            line = line[2:-1]
            line = line.split('\\n')[0]
            imageBytesArray.append(line)
    return {'img': imageBytesArray, 'header': lines[:3]}


def saveImage(header, array):
    f = open('cipherimg.pbm', 'wb')
    for line in header:
        f.write(line)
    for row in array:
        newLine = (''.join([str(byte) for byte in row]) + '\n').encode()
        f.write(newLine)
    f.close()


def getShiftedKey(key):

    temp = key[0]

    return key[1:] + temp


def getPermutation(perutation, value):
    output = ''
    for el in perutation:
        output += value[el]
    return output


def roundZero(message, results):
    l = message[0:6]
    r = message[6:]
    results.append(l)
    results.append(r)


def miniDes(r, l, key, permutation, results):
    r = getPermutation(permutation, r)

    xor = [str(ord(r[n])^ord(key[n])) for n in range(len(r))]
    xor = ''.join(xor)

    s1Index = int(xor[:4], 2)
    s2Index = int(xor[4:], 2)

    temp = str(sbox1[s1Index]+sbox2[s2Index])

    result = [str(int(temp[n]) ^ int(l[n])) for n in range(len(temp))]
    result = ''.join(result)
    results.append(result)
    return result


def xor_bytes(x1, x2):
    xor = [str(int(x1[n]) ^ int(x2[n])) for n in range(len(x1))]
    xor = ''.join(xor)
    return xor


def main(key, mode):
    IV = '111011010010'
    cipherImg = []
    data = prepareImage()
    imgData = data['img']

    for line in imgData:
        outputLine = ''
        length = len(line)
        partsNumber = int(length / 12)
        complement = ''
        if length % 12 != 0:
            for i in range(0, length-(partsNumber*12)):
                complement += '0'
            partsNumber += 1
            line += complement

        for partIndex in range(0, partsNumber):
            results = []
            keyCopy = key
            part = line[partIndex*12: (partIndex*12)+12]
            if mode == 'cbc':
                part = xor_bytes(IV, part)
            roundZero(part, results)
            for i in range(1, 8):
                keyCopy = getShiftedKey(keyCopy)

                miniDes(results[i], results[i-1], key, permutation, results)
                IV = results[-1] + results[-2]
            outputLine += IV
        cipherImg.append(outputLine[:length])
    saveImage(data['header'], cipherImg)

#mode: minides / cbc
main(key, 'cbc')