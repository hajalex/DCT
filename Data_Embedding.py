import numpy as np


def data2binary(data):
    if type(data) == str:
        p = ''.join([format(ord(i), '08b')for i in data])
    elif type(data) == bytes or type(data) == np.ndarray:
        p = [format(i, '08b')for i in data]
    elif type(data) == int:
        p = format(data, "08b")
    else:
        return ValueError("Input Type Not Supported")
    return p

#====================================================================================================#
#====================================================================================================#

def embed_encoded_data_into_DCT2(dct_block, data):
    converted_blocks = []
    bitMess = data2binary(data)
    f = 0
    d = 0
    count=0
    while d < True:
        x = dct_block[f]
        for i in range(8):
            for j in range(8):
                if i == 0 and j == 0:
                    pass
                elif (x[i][j] == 0) or (x[i][j] == 1):
                    pass
                elif (x[i][j] == -0) or (x[i][j] == -1):
                    pass
                elif d < len(bitMess):
                    digit = bitMess[d]
                    sd = data2binary(int(x[i][j]))
                    sd = list(sd)
                    sd[-1] = digit
                    sd = "".join(sd)
                    sd = bin(int(sd, 2))
                    sd = int(sd, 2)
                    x[i][j] = float(sd)
                    d += 1
        f += 1
    for quantizedBlock in dct_block:
        for i in range(8):
            for j in range(8):
                if i == 0 and j == 0:
                    pass
                elif (x[i][j] == 0) or (x[i][j] == 1):
                    pass
                elif (x[i][j] == -0) or (x[i][j] == -1):
                    pass
                else :
                    count+=1
        converted_blocks.append(quantizedBlock)
    return converted_blocks
    

def extract_encoded_data_from_DCT1(dct_blocks):
    messSize = None
    messageBits = []
    buff = 0
    i = 0
    x = []
    for quantizedBlock in dct_blocks:
        DC = quantizedBlock[0][7]
        DC = np.uint8(DC)
        DC = np.unpackbits(DC)
        if DC[7] == 1:
            buff += (0 & 1) << (7-i)
        elif DC[7] == 0:
            buff += (1 & 1) << (7-i)
        i = 1+i
        if i == 8:
            messageBits.append(chr(buff))
            buff = 0
            i = 0
            if messageBits[-1] == '*' and messSize is None:
                try:
                    messSize = int(''.join(messageBits[:-1]))
                except:
                    pass
        if len(messageBits) - len(str(messSize)) - 1 == messSize:
            return ''.join(messageBits)[len(str(messSize))+1:]
    return messageBits