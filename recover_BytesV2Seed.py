#!/usr/bin/env python3
from functions import *
import random

SEED = b"my seed"
random.seed(SEED)
# k = 18
# K = [0xc83476be, 0x9f313ec1, 0xfdb09e63, 0xf3827c68, 0x7814c985, 0xb1e9e888, 0xa924e2f8, 0x1fe1760b, 0xca754857, 0x67433568, 0x287bc567, 0xaba62218, 0xf1a54538, 0xba893a44, 0x41256723, 0xc046d021, 0x73656564, 0x6d7920]

S = [untemper(random.getrandbits(32)) for _ in range(624)]

# because the seed has only 7 chars it can be recovered using 8 carefully chosen outputs
I_230_, I_231 = invertStep(S[3], S[230])
I_231_, I_232 = invertStep(S[4], S[231])
I_232_, I_233 = invertStep(S[5], S[232])
I_233_, I_234 = invertStep(S[6], S[233])

I_231 += I_231_
I_232 += I_232_
I_233 += I_233_


# K[16] + 16
seed_l = recover_Kj_from_Ii(I_233, I_232, I_231, 233) - 16
# K[17] + 17
# two possibilities for I_234
seed_h1 = recover_Kj_from_Ii(I_234, I_233, I_232, 234) - 17
seed_h2 = recover_Kj_from_Ii(I_234+0x80000000, I_233, I_232, 234) - 17

seed1 = (seed_h1 << 32) + seed_l
seed2 = (seed_h2 << 32) + seed_l

# only the MSB of K[17] differs
print(bytes.fromhex(hex(seed1)[2:]))
print(bytes.fromhex(hex(seed2)[2:]))


