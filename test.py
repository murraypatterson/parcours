
import sys
from ete3 import Tree
from itertools import product
from sympy.utilities.iterables import multiset_permutations
import numpy

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
# produce a multiset from a set a and its multiplicities
def multi(a, ms) :

    s = []
    for x,y in zip(a, ms) :
        s += [x] * y

    return s

#
# the \otimes operator of the manuscript (a kind of "cartesian
# product")
def otimes(S, T) :

    return [{**s, **t} for s in S for t in T]

#
# pretty print the entries of a dictionary
def p_d(d) :

    return '{' + ', '.join('{}:{}->{}'.format(x,d[x][0],d[x][1]) for x in d) + '}'

#
# pretty print a list of dictionaries (an entry w of dp table)
def p_w(w) :

    return '[' + ', '.join(p_d(d) for d in w) + ']'

#
# print an entry of the dp table (for debugging purposes)
def p_dp(u, sigma, rs) :

    return 'w[{}][{}][{}] = {}'.format(u, sigma, rs, p_w(w[u][sigma][rs]))

#
# W_u(r_1, ..., r_m | sigma)
def W(u, sigma, rs, debug = False) :
    result = []

    if debug :
        print()
        print()
        print('w[{}][{}][{}] = U'.format(u.name, sigma, rs))

    V = u.get_children()
    n = len(V)

    to = sorted(set(alpha) - set([sigma]))
    rsd = {t : r for t,r in zip(ts,rs)}
    c = [rsd[(sigma,x)] for x in to]

    # s in S
    for ms in bars_and_stars(k-1, n, c) :
        s = multi(to + [sigma], ms)

        # r_1', ..., r_m'
        rpsd = {t : rsd[t] for t in ts}
        for j in range(len(to)) :
            rpsd[(sigma,to[j])] -= ms[j]

        # p_1 in P_V(r_1') ... p_m in P_V(r_m')
        for ps in product(*(bars_and_stars(n-1, rpsd[t]) for t in ts)) :

            # pi in Pi(s)
            for pi in multiset_permutations(s) :

                prod = [{}]
                for i, v in enumerate(V) :

                    if pi[i] == sigma :
                        continue

                    prod[0][v.name] = (sigma, pi[i])

                if debug :
                    print()
                    print(' ', p_w(prod))

                for i, v in enumerate(V) :
                    prod = otimes(prod, w[v.name][pi[i]][tuple(p[i] for p in ps)])

                    if debug :
                        print('    x', p_dp(v.name, pi[i], tuple(p[i] for p in ps)))

                if debug :
                    print('  =', p_w(prod))

                result += prod

    if debug :
        print()
        print('=', p_w(result))

    return result

#
# obtain the alphabet: set of unique strings from a set of lines
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

# Main
#----------------------------------------------------------------------

tree = Tree(sys.argv[1], format = 8)
alpha = get_alphabet(open(sys.argv[2],'r'))
k = len(alpha)
ts = get_transitions(alpha)
s = 3 # parsimony score (+1)

print()
print('tree:', tree)
print()
print('alphabet:', alpha)
print()
print('transitions:', ts)
print()

w = {} # dp table
for node in tree.traverse('postorder') :

    w[node.name] = {a : numpy.ndarray(shape=tuple(s for t in ts), dtype=object) for a in alpha}

    # base case
    if node.is_leaf() :

        for a in alpha :
            for rs in product(range(s), repeat = len(ts)) :
                w[node.name][a][rs] = []

            w[node.name][a][tuple(0 for t in ts)] = [{}]

        continue

    # recursive case
    for a in alpha :            
        for rs in product(range(s), repeat = len(ts)) :
            w[node.name][a][rs] = W(node, a, rs, debug = True)

# verify
for node in tree.traverse('postorder') :
    print()

    for a in alpha :
        print()

        for rs in product(range(s), repeat = len(ts)) :
            print(p_dp(node.name, a, rs))
