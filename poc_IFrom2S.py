#!/usr/bin/env python3
from functions import *
import random

I = random.getstate()[1]
# this will force a state update
random.random()
S = random.getstate()[1]

for i in range(227, 240):
    Ii, Ii1 = invertStep(S[i], S[i-227])
    print(f"{Ii} == {I[i]&0x80000000}")
    print(f"{Ii1} == {I[i+1]&0x7FFFFFFF}")