import math
def readInput(keyFilePath,textFilePath):
    key = open(keyFilePath,mode='r')
    text = open(textFilePath,mode='r')
    return [key.read().split(','),text.read()]

def modularExponentiation(public_exponent,public_modulus,value):
    binary_exponent = bin(public_exponent)[:1:-1]
    powerList=[value]
    for i in range(1,len(binary_exponent)):
        powerList.append((powerList[i-1]*powerList[i-1])%public_modulus)
    
    lastValidIndex=-1
    tempVal=0
    for i in range(len(binary_exponent)):
        if int(binary_exponent[i])==1:
            if lastValidIndex==-1:
                lastValidIndex=i
                tempVal=powerList[i]
            else:
                tempVal=(powerList[i]*tempVal)%public_modulus

    return tempVal


def RSA_encrypt():
    """Encrypts a message using RSA encryption.

    Converts the characters of the message into their ascii values and concatenates these 
    into the largest block possible such that no block is larger than the public modulus.
    These blocks are then RSA encrypted and written to the ciphertext file.

    """
    data = readInput('public_key.txt','message.txt')    

    #Checks that the public modulus is big enough to encompass all the ascii values.
    if int(data[0][0])<257:
        raise ValueError

    #Generates an array whose successive items consist of the ascii values of successive
    #characters in the message.
    asciiEncoded = []
    for i in data[1]:
        asciiEncoded.append(str(ord(i)).zfill(3))
    print(asciiEncoded)

    #Works out how many characters can be concatenated for encryption.
    blocksPerElem=math.floor(len(data[0][0])/3)        
    if len(data[0][0])%3==0:
        if int(data[0][0][:3])<256:
            blocksPerElem-=1

    #Constructs the list of concatenated ascii values.
    encodedMessage=[]
    for i in range(math.ceil(len(asciiEncoded)/blocksPerElem)):
        encodedMessage.append(''.join(asciiEncoded[blocksPerElem*i:blocksPerElem*(i+1)]))        
    print(encodedMessage)
    
    #Encrypts the elements of encodedMessage.
    encryptedMessage=[]
    for i in range(len(encodedMessage)):
        encryptedMessage.append(int(encodedMessage[i]))
        #for y in range(int(data[0][1])-1):
            #encryptedMessage[i]=encryptedMessage[i]*int(encodedMessage[i])

        encryptedMessage[i]=modularExponentiation(int(data[0][1]),int(data[0][0]),encryptedMessage[i])

        #encryptedMessage[i]=encryptedMessage[i]%int(data[0][0])
    print(encryptedMessage)

    #Writes the result to the ciphertext file.
    f=open('ciphertext.txt',mode='w')
    for item in encryptedMessage:
        f.write("%s" % str(item).zfill(3*blocksPerElem))
        f.write(",")

#TODO:change decryption method to use modular exponentiation instead of doing all powers then modulo.   
def RSA_decrypt():
    """Decrypts a message that was encrypted with RSA encryption.

    Converts the characters of the message into their ascii values and concatenates these 
    into the largest block possible such that no block is larger than the public modulus.
    These blocks are then RSA encrypted and written to the ciphertext file.

    """
    data = readInput('private_key.txt','ciphertext.txt')
    public_modulus=int(data[0][0])*int(data[0][1])

    #Parses the ciphertext and generates the list encryptedMessage where each item is an
    #encrypted block of ascii values
    encryptedMessage=[]
    valStore=[]
    for i in range(len(data[1])):
        try:
            int(data[1][i])
            valStore.append(data[1][i])
            if i==len(data[1])-1:
                encryptedMessage.append(int(''.join(valStore)))
                valStore=[]
        except ValueError:
            if valStore==[]:
                pass
            else:
                encryptedMessage.append(int(''.join(valStore)))
                valStore=[]

    #Calculates the private key.
    for i in range(public_modulus):
        if ((int(data[0][2])*i)-1)%((int(data[0][0])-1)*(int(data[0][1])-1))==0:
            private_key=i

    #Decrypts the values of the ciphertext to get the concatenated blocks of ascii values.
    for x in range(len(encryptedMessage)):
        encryptedMessage[x]=str(modularExponentiation(private_key,public_modulus,encryptedMessage[x]))
     
    print(encryptedMessage)

    #De-concatenates the ascii values and puts the corresponding characters of the message
    #in the decryptedMessage array.
    decryptedMessage=[]
    valueStore=[]
    for i in range(len(encryptedMessage)-1,-1,-1):
        
        for y in range(len(encryptedMessage[i])-1,-1,-1):
            valueStore.append(encryptedMessage[i][y])
            if len(valueStore)==3 or y==0:
                print(type(valueStore),valueStore)
                valueStore.reverse()
                decryptedMessage.append(chr(int(''.join(valueStore))))
                valueStore=[]
    decryptedMessage.reverse()

    #Writes the message to a file.
    f=open('decrypt.txt',mode='w')
    for item in decryptedMessage:
        f.write("%s" % item)
        
    print(''.join(decryptedMessage))

#RSA_encrypt()    
#RSA_decrypt()
