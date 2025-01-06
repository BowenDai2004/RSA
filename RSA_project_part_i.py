"""
Bowen Dai
RSA project part i
Goal:
This file is the set-up of RSA which contains the following functions:
    - check_prime: return True if the input is prime, return False if the input is composite
    - two_primes: generate two primes of the size about 2^(input of the function)
    - generate_key: generate public and private keys of RSA
    - encrypt: encrypt the given message with the given public key
    - decrypt: decrypt the given code with the given private key
"""

import math
import random

def check_prime(n: int):
    """
    This function uses trial division to check if the number n is prime. 
    If n is prime, return True. If n is not prime, return False.
    """
    if n > 1 :
        upper_bound = math.isqrt(n) + 1
        for i in range(2, upper_bound):
            if n % i == 0:
                return False        
        return True
    else: 
        return False

def two_primes(a: int):
    """
    This function randomly selects distinct primes of size about 2^a.
    """
    random_int = random.randint(2**(a-1), 2**(a+1))
    while not check_prime(random_int):
        """
        keep chosing if the random number is not a prime
        """
        random_int = random.randint(2**(a-1), 2**(a+1))
    p = random_int

    while not check_prime(random_int) or random_int == p:
        """
        keep chosing if the random number is not a prime or the current number is the same number as the previous number.
        """
        random_int = random.randint(2**(a-1), 2**(a+1))
    q = random_int

    return p, q

def gcd(a,b):
    """
    input a, b : any positive integer
    return: the greatest common divisor of a and b
    This function use recursion to find the gcd of a and b. If b = 0, this recursion is finished and the function returns the value of a. 
    If b does not equals to zero, the function calls itself with the input of b and a(mod b).
    """
    if b == 0:
        return a
    else:
        return gcd(b, a % b)
    

def generate_key(p: int, q: int):
    """
    This key generating function takes two primes p and q and returns a tupe of town tuples. 
    The first tuple is the public key (m, k) and the second tuple is the private key (p, q, e).
    """
    m = p * q
    φ_m = (p - 1) * (q - 1)
    k = random.randint(2, φ_m)
    while gcd(φ_m, k) != 1:
        k = random.randint(2, φ_m)
    e = pow(k, -1, φ_m)
    
    return ((m ,k), (p, q, e))


def encrypt (public_key: tuple[int, int], message: int):
    """
    This function encrypts a message using the given public key. 
    The message input into this message should be one block from a possibly longer message.
    """
    public_exponent = public_key[1]
    modulo = public_key[0]
    encrypted_message = (message**public_exponent) % modulo

    return encrypted_message


def decrypt(private_key: tuple[int, int, int], encrypteed_message: int):
    """
    This function decryptes an encrypted messafe using the given private key. 
    The message input into this encrypted messafe should be one block from a possibly longer encrypted message.
    """
    private_exponent = private_key[2]
    modulo = private_key[0] * private_key[1]
    message = pow(encrypteed_message, private_exponent, mod=modulo)

    return message
