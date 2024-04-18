#!/usr/bin/env python3
from functions import *
import random

def V1(a):
    """
    Copy of Random.seed in the case of bytes and version 1.
    """
    a = a.decode('latin-1') if isinstance(a, bytes) else a
    x = ord(a[0]) << 7 if a else 0
    for c in map(ord, a):
        x = ((1000003 * x) ^ c) & 0xFFFFFFFFFFFFFFFF
    x ^= len(a)
    a = -2 if x == -1 else x
    return a

SEED = b"my seed"
# We can't recover the original seed in this case, just the equivalent 64-bit integer
print(f"{hex(V1(SEED)) = }")
random.seed(SEED, version=1)
# k = 2
# K = [0x4527321a, 0xe833f9ce]

S = [untemper(random.getrandbits(32)) for _ in range(624)]

I_227_, I_228 = invertStep(S[0], S[227])
I_228_, I_229 = invertStep(S[1], S[228])
I_229_, I_230 = invertStep(S[2], S[229])
I_230_, I_231 = invertStep(S[3], S[230])

I_228 += I_228_
I_229 += I_229_
I_230 += I_230_

# K[1] + 1
seed_h = recover_Kj_from_Ii(I_230, I_229, I_228, 230) - 1
# K[0] + 0
# two possibilities for I_231
seed_l1 = recover_Kj_from_Ii(I_231, I_230, I_229, 231)
seed_l2 = recover_Kj_from_Ii(I_231+0x80000000, I_230, I_229, 231)

seed1 = (seed_h << 32) + seed_l1
seed2 = (seed_h << 32) + seed_l2

# only the MSB of K[0] differs
print(hex(seed1), hex(seed2))


