
import sys
from ete3 import Tree
from itertools import product
from sympy.utilities.iterables import multiset_permutations

#
# obtain the alphabet: set of unique string from a set of lines
def get_alphabet(lines) :

    alpha = set([])

    for line in lines :
        alpha.add(line.strip())

    return sorted(alpha)

#
# obtain transitions from an alphabet: number of pairs (a,b) where b
# is different from a
def get_transitions(alpha) :

    return sorted([(a,b) for a in alpha for b in alpha if b != a])

#
# bars and stars with a restriction for each bar --- adapted from:
# https://stackoverflow.com/questions/28965734/general-bars-and-stars
def bars_and_stars(bars, stars, restriction = [], prefix = []) :

    if stars == 0 :
        yield prefix + [0]*(bars+1)
        return

    if bars == 0 :
        yield prefix + [stars]
        return

    bound = stars + 1
    depth = len(prefix)
    if depth < len(restriction) :
        if restriction[depth] + 1 < bound :
            bound = restriction[depth] + 1

    for i in range(bound) :
        yield from bars_and_stars(bars-1, stars-i, restriction, prefix + [i])

#
# if any element of counts dictionary rs is non-zero
def non_zero(rs) :

    for t in ts :
        if rs[t] > 0 :
            return False

    return True

#
# produce a multiset from a set a and its multiplicities
def multi(a, ms) :

    s = []
    for i in range(len(a)) :
        s += ms[i] * [a[i]]

    return s

#
# W_u(r_1, ..., r_m | sigma)
def w(u, rs, sigma) :

    if u.is_leaf() :
        if non_zero(rs) :
            return []

    else :

        v = u.children
        n = len(v)

        to = sorted(set(alpha) - set([sigma]))
        c = [rs[(sigma,x)] for x in to]

        # s \in S
        for ms in bars_and_stars(k-1, n, c) :
            s = multi(to + [sigma], ms)

            # r_1', ..., r_m'
            rsp = {t:rs[t] for t in ts}
            for i in range(len(to)) :
                rsp[(sigma,to[i])] -= ms[i]

            print(s)
            print(rsp)
            # p_1 \in P_V(r_1') ... p_m \in P_V(r_m')
            for ps in product(*(bars_and_stars(n-1, rsp[t]) for t in ts)) :

                for pi in multiset_permutations(s) :

                    print(ps, pi)
                

# Main

tree = Tree(sys.argv[1], format = 8)
alpha = get_alphabet(open(sys.argv[2],'r'))
k = len(alpha)
ts = get_transitions(alpha)
rs = {t:2 for t in ts}

print(tree)
print()
print(alpha)
print()
print(ts)
print()
print(rs)
print()

ways = w(tree, rs, 'a')
