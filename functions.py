def unshiftRight(x, shift):
    res = x
    for i in range(32):
        res = x ^ res >> shift
    return res


def unshiftLeft(x, shift, mask):
    res = x
    for i in range(32):
        res = x ^ (res << shift & mask)
    return res


def untemper(v):
    v = unshiftRight(v, 18)
    v = unshiftLeft(v, 15, 0xefc60000)
    v = unshiftLeft(v, 7, 0x9d2c5680)
    v = unshiftRight(v, 11)
    return v


def invertStep(si, si227):
    # S[i] ^ S[i-227] == (((I[i] & 0x80000000) | (I[i+1] & 0x7FFFFFFF)) >> 1) ^ (0x9908b0df if I[i+1] & 1 else 0)
    X = si ^ si227
    # we know the LSB of I[i+1] because MSB of 0x9908b0df is set, we can see if the XOR has been applied
    mti1 = (X & 0x80000000) >> 31
    if mti1:
        X ^= 0x9908b0df
    # undo shift right
    X <<= 1
    # now recover MSB of state I[i]
    mti = X & 0x80000000
    # recover the rest of state I[i+1]
    mti1 += X & 0x7FFFFFFF
    return mti, mti1


def init_genrand(seed):
        MT = [0] * 624
        MT[0] = seed & 0xffffffff
        for i in range(1, 623+1): # loop over each element
            MT[i] = ((0x6c078965 * (MT[i-1] ^ (MT[i-1] >> 30))) + i) & 0xffffffff
        return MT


def recover_kj_from_Ji(ji, ji1, i):
    # ji => J[i]
    # ji1 => J[i-1]
    const = init_genrand(19650218)
    key = ji - (const[i] ^ ((ji1 ^ (ji1 >> 30))*1664525))
    key &= 0xffffffff
    # return K[j] + j
    return key


def recover_Ji_from_Ii(Ii, Ii1, i):
    # Ii => I[i]
    # Ii1 => I[i-1]
    ji = (Ii + i) ^ ((Ii1 ^ (Ii1 >> 30)) * 1566083941)
    ji &= 0xffffffff
    # return J[i]
    return ji


def recover_Kj_from_Ii(Ii, Ii1, Ii2, i):
    # Ii => I[i]
    # Ii1 => I[i-1]
    # Ii2 => I[i-2]
    # Ji => J[i]
    # Ji1 => J[i-1]
    Ji = recover_Ji_from_Ii(Ii, Ii1, i)
    Ji1 = recover_Ji_from_Ii(Ii1, Ii2, i-1)
    return recover_kj_from_Ji(Ji, Ji1, i)


def rewindState(state):
    prev = [0]*624
    # copy to not modify input array
    s = state[:]
    I, I0 = invertStep(s[623], s[396])
    prev[623] += I
    # update state 0
    # this does nothing when working with a known full state, but is important we rewinding more than 1 time
    s[0] = (s[0]&0x80000000) + I0
    for i in range(227, 623):
        I, I1 = invertStep(s[i], s[i-227])
        prev[i] += I
        prev[i+1] += I1
    for i in range(227):
        I, I1 = invertStep(s[i], prev[i+397])
        prev[i] += I
        prev[i+1] += I1
    # The LSBs of prev[0] do not matter, they are 0 here
    return prev


def seedArrayFromState(s, subtractIndices=True):
    s_ = [0]*624
    for i in range(623, 2, -1):
        s_[i] = recover_Ji_from_Ii(s[i], s[i-1], i)
    s_[0]=s_[623]
    s_[1]=recover_Ji_from_Ii(s[1], s[623],  1)
    s_[2]=recover_Ji_from_Ii(s[2], s_[1], 2)
    seed = [0]*624
    for i in range(623, 2, -1):
        seed[i-1] = recover_kj_from_Ji(s_[i], s_[i-1], i)
    # system overdefined for seed[0,1,623]
    seed[0] = 0
    # thus s1 = (const[1] ^ ((const[0] ^ (const[0] >> 30))*1664525))
    s1_old = ((2194844435 ^ ((19650218 ^ (19650218 >> 30))*1664525))) & 0xffffffff
    seed[1] = recover_kj_from_Ji(s_[2], s1_old, 2)
    seed[623] = (s_[1] - (s1_old ^ ((s_[0] ^ (s_[0] >> 30))*1664525))) & 0xffffffff
    # subtract the j indices
    if subtractIndices:
        seed = [(2**32+e-i)%2**32 for i,e in enumerate(seed)]
    return seed


def seedArrayToInt(s):
    seed = 0
    for e in s[::-1]:
        seed += e
        seed <<= 32
    return seed >> 32