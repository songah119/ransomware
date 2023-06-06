from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# RSA키로 암호화된 키를 가져온다
file_in = open("key.bin", "rb")
private_key = RSA.import_key(open("private.pem").read())
enc_data = file_in.read(private_key.size_in_bytes())
cipher_rsa = PKCS1_OAEP.new(private_key)
data = cipher_rsa.decrypt(enc_data)     # 비밀키로 복호화
file_in.close()
# key.txt 를 생성하고 해당 파일에 쓰기
fid = open("key.txt", "wb")
fid.write(data)
