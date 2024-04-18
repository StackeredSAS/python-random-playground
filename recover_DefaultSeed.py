#!/usr/bin/env python3
from functions import *
import random

# random is not manually seeded so it uses 624 random values

S = [untemper(random.getrandbits(32)) for _ in range(624)]
I = rewindState(S)

print("Normal run :")

print(random.getrandbits(32))
print(random.random())
print(random.randbytes(4).hex())
print(random.randrange(1, 100000))

print("\nReseeded run :")

seed_array = seedArrayFromState(I)
seed = seedArrayToInt(seed_array)

# the recovered seed is very big. Too big to be printed in decimal
# print(hex(seed))
# The recovered seed is not exactly the same, but is equivalent.
random.seed(seed)

S_ = [untemper(random.getrandbits(32)) for _ in range(624)]

assert(S_ == S)

print(random.getrandbits(32))
print(random.random())
print(random.randbytes(4).hex())
print(random.randrange(1, 100000))
