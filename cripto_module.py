import base64
import hashlib
import json
from Cryptodome import Random
from Cryptodome.Cipher import AES, DES, DES3


def encrypt_file(filename,enc_algorithm,key):

    with open(filename,'r',encoding="utf8") as fo:
        data = fo.read()

    if(enc_algorithm=='AES'):

        aes = AESCipher(key)
        cipher = aes.encrypt(data)
        with open(filename[:-4]+".enc",'wb') as fo:
            fo.write(cipher)

    elif(enc_algorithm=='DES'):

        des = DESCipher(key)
        cipher = des.encrypt(data)
        with open(filename[:-4] + ".enc",'wb') as fo:
            fo.write(cipher)

    elif(enc_algorithm=='Triple DES'):
        des3 = DES3Cipher(key)
        cipher = des3.encrypt(data)
        with open(filename[:-4] + ".enc",'wb') as fo:
            fo.write(cipher)




def decrypt_file(filename,enc_algorithm,key):

    with open(filename,'rb') as fo:
        data = fo.read()

    text = ""

    if(enc_algorithm=='AES'):
        aes = AESCipher(key)
        try:
            text = aes.decrypt(data)
        except Exception as e:
            print("Are you Trying to decrypt with wrong algorithm ??\nJust asking..")

        with open(filename[:-4]+".dec",'wb') as fo:
            fo.write(text)

    elif(enc_algorithm=='DES'):
        des = DESCipher(key)
        try:
            text = des.decrypt(data)
        except Exception as e:
            print("Are you Trying to decrypt with wrong algorithm ??\nJust asking..")


        with open(filename[:-4] + ".dec",'wb') as fo:
            fo.write(text)

    elif(enc_algorithm=='Triple DES'):
        des3 = DES3Cipher(key)
        try:
            text = des3.decrypt(data)
        except Exception as e:
            print("Are you Trying to decrypt with wrong algorithm ??\nJust asking..")

        with open(filename[:-4] + ".dec",'wb') as fo:
            fo.write(text)


    if(len(text)==0):
        raise UserWarning("Might be wrong key...")





class AESCipher:    #AES in Cipher Block Chaining Mode

    def __init__( self, key ):
        self.block_size = 16
        self.key = hashlib.sha256(key.encode('utf-8')).digest()

    def encrypt( self, raw ):
        print("AES key ", self.key)
        raw = pad(raw,self.block_size)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new( self.key, AES.MODE_CBC, iv )
        return base64.b64encode( iv + cipher.encrypt( raw.encode('utf8') ) )

    def decrypt( self, enc ):
        print("AES key ", self.key)
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv )
        return unpad(cipher.decrypt(enc[16:]),self.block_size)


    #DES in Output FeedBack Mode
class DESCipher:

    def __init__(self,key):
        self.block_size = 8             #Generation 8 byte DES key
        self.key = base64.b64encode(bytes(key,'utf-8'))[0:self.block_size]

    def encrypt(self,data):
        print("DES key ", self.key)
        data = pad(data,self.block_size);
        byte_data = bytes(data, 'utf-8')
        cipher = DES.new(self.key,DES.MODE_ECB)
        return bytes(cipher.encrypt(byte_data))

    def decrypt(self,enc):
        print("DES key ", self.key)
        cipher = DES.new(self.key,DES.MODE_ECB)
        byte_enc = cipher.decrypt(bytes(enc))
        return bytes(unpad(byte_enc,self.block_size))

                #Triple DES in Cipher Block Chaining Mode
class DES3Cipher:

    def __init__(self,key):
        self.block_size = 8             #Generation 16 Byte key
        self.key = hashlib.sha256(key.encode('utf-8')).hexdigest()[:16].upper()

    def encrypt(self,data):
        print("DES3 key " , self.key)    #Padding data to block size
        data = pad(data,self.block_size);
        iv = Random.new().read(self.block_size)
        byte_data = bytes(data, 'utf-8')
        cipher = DES3.new(self.key,DES3.MODE_CBC,iv)
        return bytes(iv + cipher.encrypt(byte_data))

    def decrypt(self,enc):
        print("DES3 key ", self.key)
        iv = enc[:self.block_size]
        cipher = DES3.new(self.key,DES3.MODE_CBC,iv)
        byte_enc = unpad(cipher.decrypt(enc[self.block_size:]),self.block_size)
        return bytearray(byte_enc)


#Padding functions
def pad(s,BS):
    return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)


def unpad(s,BS):
    return s[0:-s[-1]]