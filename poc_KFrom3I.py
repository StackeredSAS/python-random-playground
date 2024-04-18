#!/usr/bin/env python3
from functions import *
import random

random.seed(12345)
# K = [12345]
# k = 1

I = random.getstate()[1]

for i in range(4, 624):
    print(i, recover_Kj_from_Ii(I[i], I[i-1], I[i-2], i))