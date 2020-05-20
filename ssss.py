# Python 3.7
"""
SSSS - Shamir's Secret Sharing Scheme
=====================================
Authors: Luca Fluri, Dominique Lagger
krysi @FHNW FS20

To install Dependencies:
pip install numpy matplotlib rich
"""
import numpy as np
import matplotlib.pyplot as plt
from random import randint
import sys
import argparse
import struct

#Console and Usage Info
p = argparse.ArgumentParser(description='A Python implementation of Shamirs Secret Sharing Algorithm.', usage='EXAMPLES: python ssss.py -g 3 5 123456789 or python ssss.py -c 3 "(57, -91.71090617482128)" "(77, -83.98436246992969)" "(89, 38.566559743382186)" "(53, -63.77746591820551)" "(25, 406.89160652231885)"', argument_default=argparse.SUPPRESS)
p.add_argument("-g", "--generate", nargs=3, help="Generate Mode, Usage: -g k n s, where k is the treshold, n the number of keys generated and s the secret")
p.add_argument("-c", "--construct", nargs="+", help="Construct Mode, Usage: -c k s0 s1 s2 ... sn, where k is the treshold and s0 to sn are the keys passed in as tuples ENCLOSED IN A STRING!")
args = p.parse_args()


max = 1000

# Polyfit precision is too low and valuespace to small to encrypt int repr. of strings => Split up
# Currently only ints with max. 8 digits decode correctly
def str2int(s):
    return int(s.encode().hex(), 16)

def int2str(i):
    return bytes.fromhex(hex(i)[2:]).decode()

def float2int(f):
    return int(round(np.longdouble(f)))


"""
Generates n keys of the k, n scheme with secret s
"""
def generateKeys(k, n, s):
    # s = str2int(s)
    s = int(s)
    # print("int: ", s)

    x = ([0] + [randint(1, max) for _ in range(k-1)]) #Generate 0 + k-1 random for interpolating random curve
    x.sort()
    y = [s] + [randint(1, max) for _ in range(k-1)] #Generate secret +  k-1 random for interpolating random curve

    p = list(map(float2int, np.polyfit(x,y,k-1, rcond=2e-32))) # Last argument is degree of polynomial
    # print(p) #Calculated Polynomial Coefficient

    f = np.poly1d(p) # So we can call f(x)

    keys = []
    asString = ""
    for i in range(n):
        x_ = randint(0, max)
        t = (x_, f(x_))
        # print(t)
        t = str(t).encode().hex()
        keys.append(t)
        asString += t + " "
        # print(t)

    print("ALL: ", asString)


    return keys #as hex representation of string from of tuples (x, f(x))

def constructSecret(k, sArray):
    if(len(sArray)<k): return None

    keys = []
    x = []
    y = []

    
    for s in sArray[:k]:
        s = bytes.fromhex(s).decode()
        # print("from hex: ", s)
        t = tuple(map(float2int, s.replace("(", "").replace(")", "").split(", ")))
        # print("converted", t) #Correct
        keys.append(t)
        x.append(t[0])
        y.append(t[1])

    # print(keys, x, y)

    p = list(map(float2int, np.polyfit(x,y,k-1, rcond=2e-32)))           # Last argument is degree of polynomial
    print(p) #Calculated Polynomial Coefficient

    f = np.poly1d(p)                # So we can call f(x)
    # print(p[-1])
    i = int(round(p[-1]))
    # print(i)
    return i
    # return int2str(i)
    # return int2str(int(round(p[-1])))


if(args.__contains__("generate")): # Generate Mode
    print("Generate Mode")
    
    k = int(args.generate[0])
    n = int(args.generate[1])
    s = str(args.generate[2])

    print("k: ", k)
    print("n: ", n)
    print("s: ", s)

    generateKeys(k, n, s)

elif(args.__contains__("construct")): # Construct Mode
    print("Construct Mode")

    k = int(args.construct[0])
    s_n = args.construct[1:]

    print("k: ", k)
    print("s_n: ", s_n)
    
    print("SECRET: ", constructSecret(k, s_n))



# #Tests
# inp = '12345678'
# for i in range(10):
#     print(int(inp) == constructSecret(2, generateKeys(2, 2, inp)))