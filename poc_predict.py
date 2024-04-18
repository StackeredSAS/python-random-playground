#!/usr/bin/env python3
from functions import *
import random

random.seed(1234)

# You don't see some of the outputs
for _ in range(1234):
    random.getrandbits(32)

# you capture 624 consecutive outputs
state = [untemper(random.getrandbits(32)) for _ in range(624)]

print("Normal run :")

print(random.getrandbits(32))
print(random.random())
print(random.randbytes(4).hex())
print(random.randrange(1, 100000))

print("\nPredicted run :")

# set RNG state from observed ouputs
random.setstate((3, tuple(state + [624]), None))

print(random.getrandbits(32))
print(random.random())
print(random.randbytes(4).hex())
print(random.randrange(1, 100000))