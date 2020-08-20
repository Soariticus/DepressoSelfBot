import random

def randHex():
    randNum = random.randint(0, 16777215)
    hexNum = str(hex(randNum))
    hexNum = '#' + hexNum[2:]
    return hexNum