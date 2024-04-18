#!/usr/bin/env python3
from functions import *
import random

I = list(random.getstate()[1][:-1])

S1 = [untemper(random.getrandbits(32)) for _ in range(624)]
S2 = [untemper(random.getrandbits(32)) for _ in range(624)]
S3 = [untemper(random.getrandbits(32)) for _ in range(624)]

# rewind once
I_ = rewindState(S1)
S2_ = rewindState(S3)
S1_ = rewindState(S2)

print(I_ == I)
print(S1_[1:] == S1[1:])
print(S2_[1:] == S2[1:])

# rewind multiple times
I_ = rewindState(rewindState(rewindState(S3)))
print(I_ == I)
print(I_[:5])
print(I[:5])
