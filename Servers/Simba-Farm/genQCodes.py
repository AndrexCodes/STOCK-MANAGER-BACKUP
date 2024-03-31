aplhabets = "ABCDEFHIJKMNOQRSTVWXYZ"
numbers = "1234567890"
string = aplhabets + numbers

import random

def genCode(num):
    code = ""
    for _ in range(num):
        code = code + random.choice(string)
    print(code)
    return code
