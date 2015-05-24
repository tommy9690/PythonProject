import requests
import traceback
import Crypto.PublicKey.RSA as RSA
import base64

#NUMBER=2
NUMBER=input("Please enter a number between 1~10000: ")
#PASSPHRASE='Hello'
PASSPHRASE=input("Please enter a passphrase: ")
PUBLIC_KEY = 'key\mykey.pem.pub'
    
def sendRequest():
    message = None
    tb = None
    enPass = encryptPassPhrase(passphrase=PASSPHRASE)
    try:
        payload = {'number': str(NUMBER), 'passphrase': enPass}
        r = requests.post('http://127.0.0.1:5001/server', params=payload)
        #print('hhheee')
        message = "Response Status Code: " + str(r.status_code) + " | " + "Prime Number Sent: " + str(NUMBER) \
                  + " | " + "PASSPHRASE Sent: " + enPass
        if r.status_code == requests.codes.ok:
            responseNumber = None
            try:
                numberPassed = int(r.content)
                responseNumber = getFibonaci(num=numberPassed)
                
            except ValueError:
                message = message + '\n' + 'Response did not return a number.'
                message = message + '\n' + 'Reason is: ' + r.text
            if not responseNumber == None:
                message = message + '\n' + "Fibonaci '" + str(numberPassed)+ "'th term is " + str(responseNumber) + '.'
		#print(message)
    except:	
        tb=traceback.format_exc()
        message = "Error when executing get!"	
    finally:
        if not tb == None:
            print(tb)	
        print(message)

#Function to get nth term of fibonaci series
def getFibonaci(num):
    nth = int(num)
    count = 3
	 
    a = 1
    b = 1
    temp = 0
    while (count <= nth):
        temp = a
        a = b
        b = a + temp
        count = count + 1
    #print(b)
    return b

#Function to read public key and encrypt String using RSA
def encryptPassPhrase(passphrase):
    encryptString = ''
    f = None
    tb = None
    try:
        f = open(PUBLIC_KEY,'r')
        pubkey = RSA.importKey(f.read())
        print("Public Key successfully imported!!")
        f.close()
        f = None
        encodeString = passphrase.encode('utf8')
        #print('EncodeString:')
        #print(encodeString)
        #print()
        
        encryptEncodeString = pubkey.encrypt(encodeString, None)[0]
        #print('encryptEncodeString:')
        #print(encryptEncodeString)
        #print()
        
        encryptStringByte = base64.encodestring(encryptEncodeString)
        #print('encryptStringByte:')
        #print(encryptStringByte)
        #print()	
        
        encryptString = encryptStringByte.decode(encoding='UTF-8')
        #print('encryptString:')
        #print(encryptString)
        #print()	

    except:
        tb=traceback.format_exc()
        print("Error in Opening File!")

    finally:
        if not tb == None:
            print(tb)	
        if not f == None:
            f.close()

    return encryptString

sendRequest()