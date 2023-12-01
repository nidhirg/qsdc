# step 1: agree on bell basis to classical bit translation
# psi-=00, psi+=01, phi-=10, phi+=11

# step 2: alice prepares N EPR pairs in psi-
# C = first particle in EPR pair, M = second particle in EPR pair, P_n(C/M) = the C/M of the nth pair

# step 3: split the pairs into the C (checking) sequence [P_1(C), P_2(C), ... P_N(C)]
#                          and the M (measure) sequence [P_1(M), P_2(M), ... P_N(M)]

# step 4: send the C sequence to bob and check for eavesdropping by:
#   a, b) bob measures a random number of C particles in a random one of the two measurement bases
#   c, d) alice measures the corresponding M particles in the same basis and checks that her result is the opposite of bobs
# With noise added, in the case that one of the bits is not flipped (there was eavesdropping or noise),
# find the probability that it was due to noise and not eavesdropping
# We can also simulate an eavesdropper and find whether our protocol successfully throws the communication out if there is eavesdropping.

# step 5: alice encodes her message on to the M sequence using unitary operations to put the EPR pair into the correct bell state
# alice also randomly encodes a random number of (sampling) pairs to be used for error checking and then transmits the M sequence to bob

# step 6: bob performs a bell-basis measurement on the sampling pairs to estimate an error rate
# the last transmission can't be used to steal info, only disturb it bc eve can only get half of the EPR pair
# so the transmission at this point is always secure, just sometimes inaccurate

# step 7: restart if error rate is too high, otherwise move on to error correction

# step 8: error correct (how?)
