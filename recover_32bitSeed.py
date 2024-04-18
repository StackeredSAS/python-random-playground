#!/usr/bin/env python3
from functions import *
import random

for i in range(16):
    random.seed(0x533D0 + i)
    # k = 1
    # K = [0x533D0+i]

    S = [untemper(random.getrandbits(32)) for _ in range(624)]

    I_227_, I_228 = invertStep(S[0], S[227])
    I_228_, I_229 = invertStep(S[1], S[228])
    I_229_, I_230 = invertStep(S[2], S[229])

    I_228 += I_228_
    I_229 += I_229_

    # two possibilities for I_230
    seed1 = recover_Kj_from_Ii(I_230, I_229, I_228, 230)
    seed2 = recover_Kj_from_Ii(I_230+0x80000000, I_229, I_228, 230)
    # only the MSB differs
    print(hex(seed1), hex(seed2))


