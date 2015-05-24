from Crypto.PublicKey import RSA

key = RSA.generate(2048)
pubkey = key.publickey()

#private key
f = open('mykey.pem.prv','w')
f.write(key.exportKey('PEM').decode(encoding='UTF-8'))
f.close()

#public key
f = open('mykey.pem.pub','w')
f.write(pubkey.exportKey('PEM').decode(encoding='UTF-8'))
f.close()