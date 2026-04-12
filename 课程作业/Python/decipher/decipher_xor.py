# -*- coding: utf-8 -*-

token = b'\x61\x62\x63\x64\x65\x66\x67\x31\x32\x33'            #'abcdefg123'
ciphertext = b'\x28\x3d\x24\x54\x0a\x12\x38\x7a\x57\x4a'

#result = ''.join(chr(ord(token[i]) ^ ciphertext[i]) for i in range(10))
result = ''.join( chr(token[i] ^ ciphertext[i]) for i in range(10))

print("result is: %s\n" %(result))
