# this file contains code to:
# - generate every possible coloring of Z_n, assuming three color classes
#   and given min{|R|, |G|, |B|} = r.
# - find every solution to x + y = z^2 in Z_n.
# - compare the solutions with the colorings and give us statistics.
# OEIS CERTIFIED!!!

# import itertools, this library contains lots of useful array operations,
# for example generating all possible combinations of an arrays elements.
import itertools
# math module also contains some helpful combinatorial functions
import math
# so does numpy
import numpy as np

# when generating a 3-coloring of Z_n with minimum color class size r,
# what we are doing is partitioning Z_n into 3 sets with minimum set size r.
# the number of ways you can do this is given by the "associated Stirling
# numbers of the second kind" (according to wikipedia).

# yield every possible array [r1 r2 r3] of 3 partition sizes of Z_n if the
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
    nlist = set(range(0, n))
    for size in sizes3(n, r):
        # take the [r1 r2 r3] array and remove duplicate entries
        size_uniq, counts = np.unique(size, return_counts=True)

        # if all three sizes are the same
        if len(size_uniq) == 1:
            samesize = size_uniq[0]
            # arbitrarily place 0 in the red class.
            # get all combinations of Z_n / 1 of size samesize - 1
            for R in itertools.combinations(nlist - {0}, samesize - 1):
                R = set(R) | {0} # R union {1}
                # arbitrarily place the next smallest element in green
                nlist_R = nlist - R # Z_n / R
                # get all combinations of Z_n / R / next smallest of size samesize - 1
                ns = {min(nlist_R)}
                for G in itertools.combinations(nlist_R - ns, samesize - 1):
                    G = set(G) | ns
                    # then blue is the remainder
                    B = nlist_R - G

                    yield [R, B, G]
        
        # or if two sizes are the same
        elif len(size_uniq) == 2:
            diffsize = size_uniq[counts == 1][0]
            samesize = size_uniq[counts > 1][0]

            # generate the diffsize class as R normally
            for R in itertools.combinations(nlist, diffsize):
                R = set(R)
                # now arbitrarily place the next smallest element in green
                nlist_R = nlist - R
                ns = {min(nlist_R)}
                for G in itertools.combinations(nlist_R - ns, samesize - 1):
                    G = set(G) | ns
                    B = nlist_R - G

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

# return the total number of colorings without generating them just yet
def ncolorings3(n, r):
    ncolorings = 0
    for size in sizes3(n, r):
        # take the [r1 r2 r3] array and remove duplicate entries
        size_uniq, counts = np.unique(size, return_counts=True)

        # if all three sizes are the same
        if len(size_uniq) == 1:
            samesize = size_uniq[0]
            # arbitrarily place 0 in the red class, and next smallest in green, as above
            ncolorings += math.comb(n - 1, samesize - 1) * math.comb(n - samesize - 1, samesize - 1)
        
        # or if two sizes are the same
        elif len(size_uniq) == 2:
            diffsize = size_uniq[counts == 1][0]
            samesize = size_uniq[counts > 1][0]
            # again following the pattern of combinations above
            ncolorings += math.comb(n, diffsize) * math.comb(n - diffsize - 1, samesize - 1)
        
        # or if each size is unique
        elif len(size_uniq) == 3:
            ncolorings += math.comb(n, size_uniq[0]) * math.comb(n - size_uniq[0], size_uniq[1])
        
    return ncolorings

#for size in sizes3(n, r):
#    print(size)

#print(len(list(colorings3(n, r))))

# now we want to find the number of rainbow solutions to x + y = z^2 in a given
# coloring. it is probably best to first generate a list of every solution in [n].
# considering we can really only run n < 20 it should be fast to just brute force,
# for example when n = 10 we need to only check 1000 (x, y, z)

def get_sollist(n):
    nlist = set(range(0, n))
    solns = set([])
    # for every x y z tuple from Z_n. this doesn't include repetitions like 2 + 2 = 2^2
    for x, y, z in itertools.permutations(nlist, 3):
        if (x + y) % n == (z**2) % n:
            # add to set of solutions (which are sets themselves)
            solns = solns | {frozenset({x, y, z})}
    
    return solns

n = 15
r = 1

#for sol in get_sollist(n):
#    print(sol)

#for coloring in colorings3(n, r):
#    print(coloring)

# now for every coloring, we want to look for the number of rainbow solutions.
# for now the program will just print some stats about this.
print(f'Z_{n}, minimum color class size r = {r}, 3 colors (RGB)')

sols = get_sollist(n)
n_color = ncolorings3(n, r)

print(f'Total number of colorings of Z_{n} = {n_color}')
print(f'Total number of solutions in Z_{n} = {len(sols)}')

# does this coloring contain a rainbow solutions?
def hasrb(coloring):
    R, G, B = coloring
    # get all x y z tuples from the coloring, where x y z are different colors
    for rainbow in itertools.product(R, G, B):
        # if the x y z is in the list of solutions
        if set(rainbow) in sols:
            return True, set(rainbow)
    
    return False, {}

n_rbcolor = 0 # total number of rainbow-free colorings
rb_colorings = [] # list of all rainbow-free colorings

n_cnt = 0
for coloring in colorings3(n, r):
    n_cnt += 1
    print(f'\rColoring {n_cnt}/{n_color} ({(100 * n_cnt/n_color):.2f} %) being checked...', end = '', flush=True)

    rb, sol = hasrb(coloring)
    if not rb:
        rb_colorings.append(coloring)
        n_rbcolor += 1

print()

for coloring in rb_colorings:
    R, G, B = coloring

    # construct array of R G B
    # silly formatting to make R G B appear in that order
    if 0 in R:
        RR = R
        if min(G) > min(B):
            GG = G
            BB = B 
        else:
            GG = B 
            BB = G 
    elif 0 in G:
        RR = G
        if min(R) > min(B):
            GG = R 
            BB = B 
        else:
            GG = B 
            BB = R 
    else:
        RR = B 
        if min(R) > min(G):
            GG = R 
            BB = G 
        else:
            GG = G 
            BB = R


    RGBs = [0] * n
    for i in range(0, n):
        if i in RR:
            RGBs[i] = 'R'
        elif i in GG:
            RGBs[i] = 'G'
        elif i in BB:
            RGBs[i] = 'B'

    print(f'Coloring: {' '.join(map(str, range(0, n)))}')
    print(f'          {' '.join(RGBs)}')


print(f'Total number of colorings = {n_color}')
print(f'Total number of rainbow-free colorings = {n_rbcolor}')
print(f'Percentage w/ rainbow solutions = {(100 * n_rbcolor / n_color):.2f} %')