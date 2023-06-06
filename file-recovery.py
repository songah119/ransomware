from base64 import b64decode
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import glob
import os

# 키 값
f = open('key.txt','rt')
recovery_key = f.read()
key_dec = b64decode(recovery_key)
f.close()

files = glob.glob('*.enc')
for file in files:
    iv = b'.m\xc5\x9c\xfd\xe9""\xe0e\xa6Do\x95A\xe9'    # iv 값
    cipher = AES.new(key_dec, AES.MODE_CBC, iv)    # AES cipher 생성
    file_name_without_enc = file[0:-4]
    txt_filepath = os.path.join(file_name_without_enc+"dec.txt")    # 파일을 생성했다
    fid = open(txt_filepath, "wb")
    with open(file, 'rb') as f:
        data = f.read()
        ct_dec = b64decode(data)     # base64 디코드
        pt = unpad(cipher.decrypt(ct_dec), AES.block_size)     # unpad, dec
        fid.write(pt)
    fid.close()

