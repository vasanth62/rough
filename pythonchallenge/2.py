

def sub_cipher(text, count):
    output = ''
    for t in text:
        if t.isalnum():
            offset = ord(t)-ord('a')
            offset = (offset + count) % 26
            output += chr(ord('a')+offset)
        else:
            output += t

    return output

import string

def use_maketrans(text, count):
    inp = ''
    cipher = ''
    for i in range(26):
        inp += chr(ord('a')+i)
        cipher += chr(ord('a')+((i+count)%26))
    return text.translate(string.maketrans(inp, cipher))

text = """g fmnc wms bgblr rpylqjyrc gr zw fylb. rfyrq ufyr amknsrcpq ypc dmp. bmgle gr gl zw fylb gq glcddgagclr ylb rfyr'q ufw rfgq rcvr gq qm jmle. sqgle qrpgle.kyicrpylq() gq pcamkkclbcb. lmu ynnjw ml rfc spj."""
print sub_cipher(text, 2)
print use_maketrans(text, 2)
print use_maketrans('map', 2)

