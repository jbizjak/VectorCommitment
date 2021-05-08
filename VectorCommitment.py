import math
import sys
import re

from datetime import datetime

from Crypto.Util import number
import hashlib
import binascii
import random
import copy

import time

def current_milli_time():
    return round(time.time() * 1000)

def countTotalBits(num):
     binary = bin(num)[2:]
     return len(binary)


def verify(C, m, i, A, S, messages, e, n):

    AtoE =pow(A, e[i], n)
    newC = AtoE*pow(S[i], m, n)%n

    if(C == newC):
        return 1
    else:
        return 0

def s_gen(messages, e, a, n):
    S =[]

    for i in range(len(messages)):
        alt = a
        for j in range(len(messages)):
            if(j==i):
                continue
            alt = pow(alt, e[j], n)
        S.append(alt)
    return S

def fast_gen(primes, partial_a, n): #divide and conquer approach to generating S values
    num = len(primes)
    if num == 1:
        return [partial_a]

    A1 = []
    A2 = []

    partial_a1 = partial_a
    partial_a2 = partial_a

    for i in range(math.floor(len(primes)/2)):
        partial_a2 = pow(partial_a2, primes[i], n)
        A1.append(primes[i])
    for i in range(math.floor(len(primes)/2), len(primes)):
        partial_a1 = pow(partial_a1, primes[i], n)
        A2.append(primes[i])

    R1 = fast_gen(A1, partial_a1, n)
    R2 = fast_gen(A2, partial_a2, n)

    R = []
    for element in R1:
        R.append(element)
    for element in R2:
        R.append(element)

    return R


def commit(messages, S, n):
    c = 1
    for i in range(len(messages)):
        c = (c*pow(S[i], messages[i], n))%n
    return c

def slow_open(messages, e, a, n, i):
    prod = 1
    for j in range(len(messages)):
        if(j == i):
            continue
        alt = a
        for k in range(len(messages)):
            if(k == i or  k == j):
                continue
            alt = pow(alt, e[k], n)

        part = alt
        prod = (prod*pow(part, messages[j], n))%n

    return prod

#open using our divide and conquer
#we actually dont need to implement new algorithm to get around the fact that we need the e_i th root
#we just remove e_i from our list of primes then generate the S values
def open(messages, e, a, n, i):

    newlist = copy.deepcopy(e)
    newlist.remove(e[i])
    fgen = fast_gen( newlist, a, n)
    prod = 1

    messageInc = 0
    for j in range(len(fgen)): #raise each s to each message, need different incrementers because one S value is gone
        if(messageInc == i):
            messageInc += 1
        prod = (prod*pow(fgen[j], messages[messageInc], n))%n
        messageInc += 1

    return prod

def keygen(messages, l):
    p =number.getPrime(1024)
    q = number.getPrime(1024)
    n = p*q
    a = 5

    maxBits = l

    randprimes = []
    while True:
        tempprime = number.getPrime(maxBits + 1)
        alreadyUsed = False
        for num in randprimes:
            if tempprime == num:
                alreadyUsed = True
        if alreadyUsed:
            continue
        randprimes.append(tempprime)
        if len(randprimes) == len(messages):
            break

    S = fast_gen(randprimes, a, n)
    return n, randprimes, a, S

def text2int(text):
    num = []
    for i in text:
        num.append(int(binascii.hexlify(i.encode()), 16))
    return num

def update(c, S, oldm, newm, i, n):

    diff = pow(S[i], newm - oldm, n)
    newC = (c*diff)%n
    return newC

def updateProof(oldProof, e, oldm, newm, a, i, j, n):
    alt = a
    for k in range(len(e)):
        if(k == i or k == j):
            continue
        alt = pow(alt, e[k], n)

    rootS = alt
    right = pow(rootS, newm - oldm, n)
    full = (oldProof*right)%n
    return full


def main():
    #simple example

    messages = [12312, 132131, 5112321312324] #random messages

    n, e, a, S = keygen(messages, 30) #generate key and proof and verify it for a simple situation

    c = commit(messages, S, n)

    proof = open(messages, e, a, n, 0)
    oldProof = open(messages, e, a, n, 1) #will use later

    verified = verify(c, messages[0], 0, proof, S, messages, e, n)
    if(not verified):
        print("ERROR: couldnt verify good proof")
    else:
        print("Verifying worked")

    notverified = verify(c, messages[1], 0, proof, S, messages, e, n)
    if(notverified):
        print("ERROR: didn't reject bad proof")
    else:
        print("Rejecting bad proof works")

    newmessage = random.randint(2**10 , 2**20) #random new message, update position 0
    newC = update(c, S, messages[0], newmessage, 0, n)

    verified2 = verify(newC, newmessage, 0, proof, S, messages, e, n)
    if(not verified2):
       print("ERROR: updating made proof no longer valid")
    else:
      print("Verifying updated proof worked")

    #this time, calculate the proof not by recalculating but by updating oldProof (which we made on old messages)
    #now verify the new proof with the new c value
    newProof = updateProof(oldProof, e, messages[0], newmessage, a, 0, 1, n)
    verified3 = verify(newC, messages[1], 1, newProof, S, messages, e, n)
    if(not verified3):
        print("ERROR: updated proof rejected")
    else:
        print("updated proof works with updated commit")

    #quick sanity check, we cannot verify a message with the old proof after updating messages
    verified4 = verify(newC, messages[1], 1, oldProof, S, messages, e, n)
    if(verified4):
        print("ERROR: old proof still works")
    else:
        print("Old proof no longer works after update")


main()
