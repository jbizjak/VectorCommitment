import math
import sys
import re
from tate_bilinear_pairing import eta
from tate_bilinear_pairing import ecc
import random

def keygen(g, q):
    z=[]
    for i in range(q):
       z.append(random.randint(0,50))
    h1 = []
    for i in range(len(z)):
        h1.append(ecc.scalar_mult(z[i], g))
    h2 = []
    for i in range(len(z)):
        h2.append([])
        for j in range(len(z)):
            if(i == j):
                h2[i].append(0)
                continue
            h2[i].append(ecc.scalar_mult(z[i]*z[j], g))
    return h1, h2, z

def commit(messages, h1):
    C = ecc.scalar_mult(0, h1[0])
    for i in range(len(messages)):
        C = ecc.add(C,  ecc.scalar_mult(messages[i], h1[i]))
    return C

def open(message, i, messages, h2, g):
    print(g)
    A = ecc.scalar_mult(0, g)
    for j in range(len(messages)):
        if(i==j):
            continue
        A = ecc.add(A,  ecc.scalar_mult(messages[j], h2[i][j]))
    return A

def verify(C, message, i, A, g, h1, z):
    #TODO use a different library which supports subtraction
    denom = ecc.scalar_mult(-1, h1[i])


def main():
    eta.init(151)
    g = ecc.gen()

    h1, h2, z = keygen(g, 3)

    messages = [1, 2, 3]
    C = commit(messages, h1)

    A = open(1, 0, messages, h2, g)

    #TODO use a different library to make verification/updating work
    # if(verify(C, 1, 0, A, 5, h1, z[0])):
    #     print("verified")
    # else:
    #     print("not verified")
main()
