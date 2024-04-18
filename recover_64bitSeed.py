#!/usr/bin/env python3
from functions import *
import random

for i in range(16):
    random.seed(0xDEADBEEF000533D0 + i)
    # k = 2
    # K = [0x533D0+i, 0xDEADBEEF]

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


