import math
from math import gcd
import random
from random import randint, randrange
from sympy import factorint




def square_and_multiply(a,k,n):
    h = 1
    binary_k = bin(k)[2:]
    for bit in binary_k:
        h = (h * h) % abs(n)
        if bit == '1':
            h = (h * a) % abs(n)
    return h
    
def test_rabin(n, a):
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    x = square_and_multiply(a, d, n)
    if x in (1, n - 1):
        return False
    for _ in range(s - 1):
        x = (x * x) % n
        if x == n - 1:
            return False
    return True

def miller_rabin(n, d):
    if n == 2:
        return True
    return all(not test_rabin(n, randint(2, n - 1)) for _ in range(d))

def generate_premier(nb_bits=512):
    while True:
        nb_premier = random.getrandbits(nb_bits)
        
        if miller_rabin(nb_premier, 50):
            return nb_premier

def exp_rapide(g, n):
    if n == 0:
        return 1  # élément neutre
    e = int(math.log2(n))
    h, t = g, g
    while e > 0:
        e -= 1
        h = h*h
        if (n >> e) & 1:  # aie
            h = h * t

    return h

def ordre(a, n):
    if gcd(a, n) != 1:
        return None
    for k in range(1, n):
        if pow(a, k, n) == 1:
            return k
    return None

def calculate_generator(p):
    for i in range(2, p):
        if ordre(i, p) == p-1:
            return i

def find_generator(p):
    small_factors = factorint(p-1, limit=10**6.5).keys() # factorint retourne les facteurs premiers de n jusqu’au limit, keys() récupère uniquement les nombres premiers distincts
    # on teste pour tous les petits facteurs, on devrait tout tester mais ça coûte trop chère en temps donc on teste les plus succeptibles d'être faux : les petits facteurs -> limite à 10**6.5
    while True:
        g = randrange(2, p-1)
        g_is_a_generator = True 
        for q in small_factors: # debut du test -> théorie des groupes cycliques
            if square_and_multiply(g, (p-1)//q, p) == 1:
                g_is_a_generator = False
                break
            if g_is_a_generator:
                return g


#Simulation de l'échange de clés Diffie-Hellman entre Alice et Bob, ici, on retourne le secret partagé
def diffie_hellman(p, g, a=None, b=None):
    if a is None:
        a = randint(1, p-1)
    if b is None:
        b = randint(1, p-1)

    A = pow(g, a, p) # normalent, c'est alice qui envoie A à Bob,
    B = pow(g, b, p)  # normalement, c'est bob qui envoie B à Alice

    shared_secret_a = pow(B, a, p)
    shared_secret_b = pow(A, b, p)

    assert shared_secret_a == shared_secret_b
    return shared_secret_a