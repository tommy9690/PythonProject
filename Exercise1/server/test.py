from flask import Flask, request
import requests
import traceback
import Crypto.PublicKey.RSA as RSA
import base64

PRIVATE_KEY = 'key\mykey.pem.prv'

app = Flask(__name__)
app.config.from_object(__name__)

#Flask API, app.route define URL path 
@app.route('/server', methods=['GET','POST'])
def receive():
    message = ''
    tb = None
    #if request.method == 'POST':
    	
    if not request.args.get('passphrase') == None:
        try:
            dePass = decryptPassPhrase(request.args.get('passphrase'))
            print('Decrypted Passphrase: ' + dePass)
            if not request.args.get('number') == None:
                if validateNumberFormatString(numString=request.args.get('number')):
                    number=int(request.args.get('number'))
                    message=str(getPrime(num=number))
                else:
                    message="Number Format is wrong in 'number' attribute"
            else:
                message="No 'number' request parameter"
        except:
            message = "Error in decrypting PassPhrase!"
            tb = traceback.format_exc()
        finally:
            if not tb == None:
                print(tb)

    else:
        message="No 'passphrase' request parameter"
    #print(message)
    return message      

#Function to get the nth term of prime number
def getPrime(num):
    
    currentNum = 1
    primeCount = 0
    while (primeCount < num):
        currentNum = currentNum + 1	
        isPrime = True
        if currentNum > 2:
            for counter in range(2,currentNum):
                if currentNum % counter == 0:
	                isPrime = False
	                break
        if isPrime:
            primeCount = primeCount + 1

    print("'" + str(num) + "'th prime number is " + str(currentNum) + ".")
    return currentNum		

#Function to decrypt encrypted string using RSA
def decryptPassPhrase(enpass):
    decryptString = ''
    f = None
    tb = None
    try:
        f = open(PRIVATE_KEY,'r')
        pkey = RSA.importKey(f.read())
        print("Private Key successfully imported!!")
        f.close()
        f = None

        encryptStringUTF8Encode = enpass.encode('utf8')
        #print('encryptStringUTF8Encode:')
        #print(encryptStringUTF8Encode)
        #print()	
        
        encryptStringBase64Decode = base64.decodestring(encryptStringUTF8Encode)
        #print('encryptStringBase64Decode:')
        #print(encryptStringBase64Decode)
        #print()	
        	    
        decryptencodeString = pkey.decrypt(encryptStringBase64Decode)
        #print('decryptencodeString:')
        #print(decryptencodeString)
        #print()
	    
        decryptString = decryptencodeString.decode('utf8')
        #print('decryptString:')
        #print(decryptString)
        #print()

    finally:
        if not tb == None:
            print(tb)	
        if not f == None:
            f.close()

    return decryptString

#Function to validate the string passed is a number and between 1 to 10000 inclusive
def validateNumberFormatString(numString):
    isNumberBetOneTenThousand = False
    try:
        number = int(numString)
        if number >= 1 and number <= 10000:
            isNumberBetOneTenThousand = True
    except ValueError as e:
        print("Can't Convert String to Number.")

    return isNumberBetOneTenThousand
        	 
#@app.route('/decrypt', methods=['GET','POST'])
#def decrypt():
#    return decryptPassPhrase(TEST)

if __name__ == '__main__':
    app.run(port=5001,debug=True)