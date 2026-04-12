# -*- coding: utf-8 -*-
# DES 加解密示例程序

from Crypto.Cipher import DES

key = b'DE3_En1C'
IDA_ciphertext = b'\xef\x34\xd4\xa3\xc6\x84\xe4\x23'

des = DES.new(key, DES.MODE_ECB)

print('Decrypted: ', des.decrypt(IDA_ciphertext))
