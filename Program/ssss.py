# Python 3.7
"""
SSSS - Shamir's Secret Sharing Scheme
=====================================
Authors: Luca Fluri, Dominique Lagger
krysi @FHNW FS20

To install Dependencies:
pip install numpy matplotlib progress



TODO Recalculate new key with k shares
"""
import numpy as np
import matplotlib.pyplot as plt
from random import randint
import sys
import argparse
import struct
from progress.bar import Bar



#Console and Usage Info
p = argparse.ArgumentParser(description='A Python implementation of Shamirs Secret Sharing Algorithm.', usage='EXAMPLE: python ssss.py -g 3 5 123456789 or python ssss.py -c 3 283739342c202d3237333629 283538392c202d3137313129 283433312c202d39323129', argument_default=argparse.SUPPRESS)
p.add_argument("-g", "--generate", nargs=3, help="Generate Shares, Usage: -g k n s, where k is the treshold, n the number of keys generated and s the secret")
p.add_argument("-c", "--construct", nargs="+", help="Construct Secret from Shares, Usage: -c k s0 s1 s2 ... sn, where k is the treshold and s0 to sn are the keys passed in")
p.add_argument("-gr", "--graph", nargs=1, help="Enables Plots, Usage: -gr 0|1")
args = p.parse_args()


max = 10000

# Polyfit precision is too low and valuespace to small to encrypt int repr. of strings => Split up
# Currently only ints with max. 20 digits decode correctly.
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

    x = [0]#([0] + [randint(1, max) for _ in range(k-1)]) #Generate 0 + k-1 random for interpolating random curve
    for _ in range(k-1): #Avoid duplicate x values
        rand = randint(1, max)
        while(x.__contains__(rand)):
            rand = randint(1, max)
        x.append(rand)
    
    # x.sort()
    y = [s] + [randint(1, max) for _ in range(k-1)] #Generate secret +  k-1 random for interpolating random curve
    # for _ in range(k-1):
    #     rand = randint(1, max)
    #     while(y.__contains__(rand)):
    #         rand = randint(1, max)
    #     y.append(rand)
    # print(x, y)


    

    p = np.polyfit(x,y,k-1) # Last argument is degree of polynomial
    # print(p) #Calculated Polynomial Coefficient

    f = np.poly1d(p) # So we can call f(x)


    

    keys = []
    keys_x = []
    keys_y = []
    asString = ""
    for i in range(n):
        x_ = randint(1, max)
        while(keys_x.__contains__(x_)): #Avoid duplicates!
            x_ = randint(1, max)
        keys_x.append(x_)
        keys_y.append(f(x_))
        t = (x_, f(x_))
        # if(args.__contains__("graph") and int(args.graph[0])): plt.plot(x_, f(x_), "go")
        # print(t)
        t = str(t).encode().hex()
        keys.append(t)
        asString += t + " "
        # print(t)

    # if(args.__contains__("graph") and int(args.graph[0])):
    # plt.plot(x, y, "b+")
    x1 = [i for i in range(max)]
    y1 = [f(x) for x in range(max)]
        # plt.plot(x1, y1, "r")

        # plt.show()

    

    # print("ALL: ", asString)


    return keys, asString, x, y, keys_x, keys_y, x1, y1 #as hex representation of string from of tuples (x, f(x))

def constructSecret(k, sArray):
    if(len(sArray)<k): return None

    keys = []
    x = []
    y = []

    
    for s in sArray[:k]:
        s = bytes.fromhex(s).decode()
        # print("from hex: ", s)
        t = tuple(map(lambda x: float(np.longdouble(x)), s.replace("(", "").replace(")", "").split(", ")))
        # print("converted", t) #Correct
        keys.append(t)
        x.append(t[0])
        y.append(t[1])

    # print(x, y)

    p = np.polyfit(x,y,k-1)          # Last argument is degree of polynomial
    # print("Coeff_dec: ", p) #Calculated Polynomial Coefficient

    f = np.poly1d(p)                # So we can call f(x)


    # if(args.__contains__("graph") and int(args.graph[0])):
    #     plt.plot(x, y, "go")
    x1 = [i for i in range(max)]
    y1 = [f(x) for x in range(max)]
        # plt.plot(x1, y1, "r")

        # plt.show()

    # print(p[-1])
    i = int(round(p[-1]))
    # print(i)
    return i, x, y, x1, y1
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

    keys, asString, x, y, keys_x, keys_y, x1, y1 = generateKeys(k, n, s)
    print(asString)
    if(args.__contains__("graph") and int(args.graph[0])):
            plt.plot(x, y, "ro")
            plt.plot(x1, y1, "r")
            plt.plot(keys_x, keys_y, "r+")
            plt.show()

elif(args.__contains__("construct")): # Construct Mode
    print("Construct Mode")

    k = int(args.construct[0])
    s_n = args.construct[1:]

    print("k: ", k)
    # print("s_n: ", s_n)
    
    secret, x_d, y_d, x1_d, y1_d = constructSecret(k, s_n)
    print("SECRET: ", secret)
    if(args.__contains__("graph") and int(args.graph[0])):
            plt.plot(x_d, y_d, "g+")
            plt.plot(x1_d, y1_d, "g")
            plt.show()

else:
    #Tests
    def test():
        print("TESTING")
        # i = 12345678 => 0.2% chance for numerical error
        # i = 1234567 => 0.04% chance for numerical error
        # i = 123456 => 0.0% chance for numerical error
        # i = 12345 => 0.0% chance for numerical error

        maxI = 12345678
        duration = 200
        errors = 0

        bar = Bar("Testing ", max = duration)
        for i in range(maxI-duration, maxI):
            i = 123456789
            keys, asString, x, y, keys_x, keys_y, x1, y1 = generateKeys(6, 10, i)
            secret, x_d, y_d, x1_d, y1_d = constructSecret(6, keys)
            # print(i, secret)
            suc = i == secret

            bar.next()
            if(not suc):
                errors += 1 
                print("ERROR", i, secret, y1[0])



                plt.plot(x, y, "ro")
                plt.plot(x1, y1, "r")
                plt.plot(keys_x, keys_y, "r+")
                plt.plot(x_d, y_d, "g+")
                plt.plot(x1_d, y1_d, "g")
                plt.show()
                break
        bar.finish()
        print(round(errors/duration * 100, 4), "% Errors")

    test()