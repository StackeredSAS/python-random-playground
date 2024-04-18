# Python random playground

This repository contains code snippets and POCs associated to our article on [breaking Python's PRNG with a few values and no bruteforce](https://stackered.com/blog/python-random-prediction/). 

The functions shared accross all POCs are located in [functions.py](./functions.py).

# POCs

- [poc_predict](./poc_predict.py) : This POC shows how to predict the futur PRNG outputs given 624 consecutive outputs.
- [poc_IFrom2S](./poc_IFrom2S.py) : This POC shows how to recover an **initial state** `I` value from a pair of **current state** `S` values.
- [poc_KFrom3I](./poc_KFrom3I.py) : This POC shows how to recover a value of `K` (the seed array) from three consecutive **initial state** `I` values.
- [poc_stateRewind](./poc_stateRewind.py) : This POC shows how to rewind a full state `S` up to the **initial state** `I`.

# Example seed recovery

- [recover_32bitSeed](./recover_32bitSeed.py) : Example recovery of a 32-bit seed using 6 outputs.
- [recover_64bitSeed](./recover_64bitSeed.py) : Example recovery of a 64-bit seed using 8 outputs.
- [recover_FloatSeed](./recover_64bitSeed.py) : Example recovery of a 64-bit seed using 8 outputs. This time the PRNG is seeded with a float.
- [recover_BytesV1Seed](./recover_BytesV1Seed.py) : Example recovery of a 64-bit seed using 8 outputs. This time the PRNG is seeded with bytes, using the version 1 algorithm.
- [recover_BytesV2Seed](./recover_BytesV2Seed.py) : Example recovery of a 7 characters long seed using 8 outputs. This time the PRNG is seeded with bytes, using the version 2 algorithm (the default).
- [recover_DefaultSeed](./recover_DefaultSeed.py) : Example recovery of the operating system's CSPRNG generated seed using 624 outputs. The PRNG is not seeded explicitely (the default case).