# Python 3.7
"""
SSSS - Shamir's Secret Sharing Scheme
=====================================
Authors: Luca Fluri, Dominique Lagger
krysi @FHNW FS20

To install Dependencies:
pip install numpy matplotlib progress

"""
import numpy as np
import matplotlib.pyplot as plt
from random import randint
import sys
import argparse
from progress.bar import Bar



#Console and Usage Info
p = argparse.ArgumentParser(description='A Python implementation of Shamirs Secret Sharing Algorithm.', usage='EXAMPLE: python ssss.py -g 3 5 123456789 or python ssss.py -c 3 283739342c202d3237333629 283538392c202d3137313129 283433312c202d39323129', argument_default=argparse.SUPPRESS)
p.add_argument("-g", "--generate", nargs=3, help="Generate Shares, Usage: -g k n s, where k is the treshold, n the number of keys generated and s the secret")
p.add_argument("-c", "--construct", nargs="+", help="Construct Secret from Shares, Usage: -c k s0 s1 s2 ... sn, where k is the treshold and s0 to sn are the keys passed in")
p.add_argument("-gr", "--graph", nargs=1, help="Enables Plots, Usage: -gr 0|1")
args = p.parse_args()


max = int(1e5)

# Polyfit precision is too low and valuespace to small to encrypt int repr. of strings => Split up
# Currently only ints with max. 20 digits decode without rounding errors.

""" 
Generates n keys of the k, n scheme with secret s
"""
def generateKeys(k, n, s):
    s = int(s)

    decodable = False

    while(not decodable):
        x = [0]
        for _ in range(k-1): #Avoid duplicate x values
            rand = randint(1, max)
            while(x.__contains__(rand)):
                rand = randint(1, max)
            x.append(rand)
        
        y = [s] + [randint(1, max) for _ in range(k-1)] #Generate secret +  k-1 random for interpolating random curve        

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
            t = str(t).encode().hex()
            keys.append(t)
            asString += t + " "


        x1 = [i for i in range(max)]
        y1 = [f(x) for x in range(max)]
        
        if(constructSecret(k, keys)[0] == s): decodable = True

    return keys, asString, x, y, keys_x, keys_y, x1, y1 #as hex representation of string from of tuples (x, f(x))



def constructSecret(k, sArray):
    if(len(sArray)<k): return None

    keys = []
    x = []
    y = []

    
    for s in sArray[:k]:
        s = bytes.fromhex(s).decode()
        t = tuple(map(lambda x: float(np.longdouble(x)), s.replace("(", "").replace(")", "").split(", ")))
        keys.append(t)
        x.append(t[0])
        y.append(t[1])


    p = np.polyfit(x,y,k-1)          # Last argument is degree of polynomial
    # print("Coeff_dec: ", p) #Calculated Polynomial Coefficient

    f = np.poly1d(p)                # So we can call f(x)

    x1 = [i for i in range(max)]
    y1 = [f(x) for x in range(max)]
        
    i = int(round(p[-1]))
    return i, x, y, x1, y1




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
            plt.plot(keys_x, keys_y, "go")
            plt.show()

elif(args.__contains__("construct")): # Construct Mode
    print("Construct Mode")

    k = int(args.construct[0])
    s_n = args.construct[1:]

    print("k: ", k)
    
    secret, x_d, y_d, x1_d, y1_d = constructSecret(k, s_n)
    print("SECRET: ", secret)
    if(args.__contains__("graph") and int(args.graph[0])):
            plt.plot(x_d, y_d, "go")
            plt.plot(x1_d, y1_d, "g")
            plt.show()

else:
    #Tests
    def test():
        print("TESTING")

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