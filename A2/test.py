import math
def checksumCalc(payload):
    #The implemention of function that calculates checksum goes here

    
    ascii_values = [ord(character) for character in payload]
    checksum = 0

    for i,v in enumerate(ascii_values): 
        checksum += v 

    print(checksum)


    return checksum


#checksumCalc("Hello")
checksumCalc("dddddddddddddddddddd")
