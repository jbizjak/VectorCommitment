# VectorCommitment

This repository has two files.

<h4>RSA implementation</h4>
VectorCommitment.py contains a vector commitment implementation based on the RSA assumption.

1024-bit primes are used to create the base N.

The Crypto library is used to generate random primes.

Almost all code follows a straightforward implementation of the implementation described in: https://www.iacr.org/archive/pkc2013/77780054/77780054.pdf

Two exception are:

1. To generate proofs, rather than finding the product then finding the e_i th root we remake the S values without raising them to the e_ith power.

2. For creating S values we use a divide and conquer approach to speed up the proccess (applies to key generation and proof generation).

<h4>CDH implementation</h4>
VectorCommitmentDH.py contains a vector commitment implementation based on the CDH assumption.


Example usage:

messages = [1, 2, 3] #create some messages

n, e, a, S = keygen(messages, len(messages)) #generate public parameters

c = commit(messages, S, n) #generate commitment

proof = open(messages, e, a, n, 0) #create opening (proof)

if(verify(c, messages[0], 0, proof, S, messages, e, n)): #should be able to verify that proof with respect to the commitment and the message
  print("sucess")
 else:
  print("failure")
