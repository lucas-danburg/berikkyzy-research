# this file contains code to:
# - generate every possible coloring of [n], assuming three color classes
#   and given min{|R|, |G|, |B|} = r.
# - find every solution to x + y = z^2 in [n].
# - compare the solutions with the colorings and give us statistics.
# OEIS CERTIFIED!!!

# import itertools, this library contains lots of useful array operations,
# for example generating all possible combinations of an arrays elements.
import itertools
# math module also contains some helpful combinatorial functions
import math
# so does numpy
import numpy as np

# when generating a 3-coloring of [n] with minimum color class size r,
# what we are doing is partitioning [n] into 3 sets with minimum set size r.
# the number of ways you can do this is given by the "associated Stirling
# numbers of the second kind" (according to wikipedia).

# yield every possible array [r1 r2 r3] of 3 partition sizes of [n] if the
# minimum partition size is r
def sizes3(n, r):
    k = 3

    # error catching
    if r > n/k:
        raise ValueError('r must be less than or equal to n/k (n/3)')
    
    # one partition will have to be the smallest, we can make that r1.
    # the smallest it can be is r, and the largest it can be is floor(n/k).
    for r1 in range(r, math.floor(n/k) + 1):
        # r2 can be the second smallest, from r1 to half of the remaining size
        for r2 in range(r1, math.floor((n - r1)/(k - 1)) + 1):
            # then r3 is the remainder
            r3 = n - r1 - r2

            yield np.array([r1, r2, r3])

# yield every possible coloring of [n] with three color classes with
# minimum class size r
def colorings3(n, r):
    nlist = set(range(1, n + 1))
    for size in sizes3(n, r):
        # take the [r1 r2 r3] array and remove duplicate entries
        size_uniq, counts = np.unique(size, return_counts=True)

        # if all three sizes are the same
        if len(size_uniq) == 1:
            samesize = size_uniq[0]
            # arbitrarily place 1 in the red class.
            # get all combinations of [n] / 1 of size samesize - 1
            for R in itertools.combinations(nlist - {1}, samesize - 1):
                R = set(R) | {1}
                # arbitrarily place the next smallest element in green
                # [n] / R
                nlist_R = nlist - R
                # get all combinations of [n] / R / next smallest of size samesize - 1
                ns = {sorted(nlist_R)[0]}
                for G in itertools.combinations(nlist_R - ns, samesize - 1):
                    G = set(G) | ns
                    # then blue is the remainder
                    B = nlist_R - G

                    yield [R, G, B]
        
        # or if two sizes are the same
        elif len(size_uniq) == 2:
            diffsize = size_uniq[counts == 1][0]
            samesize = size_uniq[counts > 1][0]

            # generate the diffsize class as R normally
            for R in itertools.combinations(nlist, diffsize):
                R = set(R)
                # now arbitrarily place the next smallest element in green
                nlist_R = nlist - R
                ns = {sorted(nlist_R)[0]}
                for G in itertools.combinations(nlist_R - ns, samesize - 1):
                    G = set(G) | ns
                    B = nlist_R - G

                    #print([R, G, B])
                    yield [R, G, B]
        
        # or if each size is unique
        elif len(size_uniq) == 3:
            # generate everything normally
            for R in itertools.combinations(nlist, size_uniq[0]):
                R = set(R)
                nlist_R = nlist - R
                for G in itertools.combinations(nlist_R, size_uniq[1]):
                    G = set(G)
                    B = nlist_R - G

                    yield [R, G, B]

n = 6
r = 1
for size in sizes3(n, r):
    print(size)

for coloring in colorings3(n, r):
    print(coloring)

print(len(list(colorings3(n, r))))

# now we want to find the number of rainbow solutions to x + y = z^2 in a given
# coloring. it is probably best to first generate a list of every solution in [n].
# considering we can really only run n < 20 it should be fast to just brute force,
# for example when n = 10 we need to only check 1000 (x, y, z)

def get_sollist(n):
    nlist = range(1, n + 1)
    solns = np.array([])
    for x, y, z in itertools.product(nlist, repeat = 3):
        if x + y == z**2:
            x = 1
