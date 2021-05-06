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
This implementation is incomplete, as the bilinear pairing library used does not support subtraction, thus updating and verifying the proofs is not possible. 

Making this work should be as simple as replacing the current pairing library but I could not get another library installed properly.


<h4>Example usage</h4>

messages = [1, 2, 3, 4] #create some messages

n, e, a, S = keygen(messages, 3) #generate public parameters, 3 is max number of bits

c = commit(messages, S, n) #generate commitment

proof = open(messages, e, a, n, 0) #create opening (proof)

#should be able to verify that proof with respect to the commitment and the message

if(verify(c, messages[0], 0, proof, S, messages, e, n)): 

  print("sucess")
  
else:
 
  print("failure")
