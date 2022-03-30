
import sys
from ete3 import Tree
from itertools import product
from sympy.utilities.iterables import multiset_permutations
import numpy
import parse

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
# a concise pretty print for an entry of a dictionary, assuming branch
# (key) is a character, and state transition (value) in binary
def p_c(b, i, j) :

    if i == alpha[0] :
        assert j == alpha[1]
        return b.upper()

    assert i == alpha[1]
    return b.lower()

#
# pretty print the entries of a dictionary
def p_d(d, math = False) :

    # an adhoc concise mode for the special case with two states
    if concisemode :
        return r'\{' + ', '.join(p_c(x,d[x][0],d[x][1]) for x in d) + r'\}'

    if math :
        return r'\{' + ', '.join(r'{}:\text{{{}}}{{\rightarrow}}\text{{{}}}'.format(x,d[x][0],d[x][1]) for x in d) + r'\}'

    return '{' + ', '.join('{}:{}->{}'.format(x,d[x][0],d[x][1]) for x in d) + '}'

#
# pretty print a list of dictionaries (an entry w of dp table)
def p_w(w, math = False) :

    s = ', '.join(p_d(d, math=math) for d in w)

    if math :
        if not s :
            return r'\0'
        if s == r'\{\}' :
            return r'\1'
        return r'\{' + s + r'\}'

    return '[' + s + ']'

#
# print an entry of the dp table (for debugging purposes)
def p_dp(u, sigma, rs, numerical = False, math = False) :

    d = w[u][sigma][rs]
    p = p_w(d, math = math)
    if numerical :
        p = len(d)

    if math :
        r = ','.join(str(x) for x in rs)
        return r'W_{}({} ~|~ \text{{{}}}) %= {}'.format(u, r, sigma, p)

    return 'w[{}][{}][{}] = {}'.format(u, sigma, rs, p)

#
# W_u(r_1, ..., r_m | sigma)
def W(u, sigma, rs, debug = False, prune = False, math = False) :
    result = []
    bsw = False
    
    if debug :
        if not math :
            print()

        print()

        out = 'w[{}][{}][{}] = U'.format(u.name, sigma, rs)
        if math :
            print(r'\begin{multline*}')
            
            r = ','.join(str(x) for x in rs)
            out = r'W_{}({} ~|~ \text{{{}}}) = \\'.format(u.name, r, sigma)

        print(out)

        if math :
            print(r'\begin{aligned}')

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

                # pi'
                base = [{}]
                prod = [{}]
                sw = False
                for i, v in enumerate(V) :

                    if pi[i] == sigma :
                        continue

                    base[0][v.name] = (sigma, pi[i])
                    prod[0][v.name] = (sigma, pi[i])

                if debug and not math :
                    print()

                # bigotimes_{v in V} W_v(p_1^v, ..., p_m^v | pi^v)
                for i, v in enumerate(V) :
                    w_v = w[v.name][pi[i]][tuple(p[i] for p in ps)]
                    prod = otimes(prod, w_v)

                    if debug :
                        pref = '     '

                        if math :
                            pref = '    &'

                            if bsw :
                                pref = r' \cup ~&'

                        if sw :
                            pref = '    x'

                            if math :
                                pref = r'   \x'
                                
                        print(pref, p_dp(v.name, pi[i], tuple(p[i] for p in ps), math = math))

                        bsw = True
                        sw = True

                    if prune and not w_v :

                        if debug :
                            print('    ..prune')

                        break

                if debug :
                    pwb = p_w(base, math = math)
                    pwp = p_w(prod, math = math)

                    if math :
                        print(r'   \x {} \\%= {}'.format(pwb, pwp))
                    else :
                        print('    x {} = {}'.format(pwb, pwp))

                result += prod

    if debug :
        if math :
            print(r'\end{aligned}\\')
        else :
            print()

        print('=', p_w(result, math=math))

        if math :
            print(r'\end{multline*}')

    return result

#
# obtain the alphabet: set of unique substrings from a string
def get_alphabet(string) :

    alpha = []
    for s in string.split() :

        if s not in alpha :
            alpha.append(s)

    return alpha

#
# obtain transitions from an alphabet: number of pairs (a,b) where b
# is different from a
def get_transitions(alpha) :

    return [(a,b) for a in alpha for b in alpha if b != a]

#
# obtain (number of) transition events from a string and create a
# dictionary in the context of a known set of transitions
def process_events(string, ts) :

    e = {t:0 for t in ts}
    for s in string.split() :

        k,a,b = parse.parse('{}:{}->{}', s)
        e[(a,b)] = int(k)

    return e

#
# Main
#----------------------------------------------------------------------

mathmode = True
concisemode = True

tree = Tree(sys.argv[1], format = 8)
alpha = get_alphabet(sys.argv[2])
k = len(alpha)
ts = get_transitions(alpha)
e = process_events(sys.argv[3], ts)

if mathmode :
    print()
    print(r'\newcommand{\0}{\emptyset}')
    print(r'\newcommand{\1}{\{\emptyset\}}')
    print(r'\newcommand{\x}{\otimes}')
    print()
    print(r'\begin{comment}')

print()
print('tree:', tree)
print()
print('alphabet:', alpha)
print()
print('transitions:', ts)
print()
print('events:', e)

if mathmode :
    print()
    print(r'\end{comment}')

w = {} # dp table
for node in tree.traverse('postorder') :

    w[node.name] = {a : numpy.ndarray(shape=tuple(e[t]+1 for t in ts), dtype=object) for a in alpha}

    # base case
    if node.is_leaf() :

        for a in alpha :
            for rs in product(*(range(e[t]+1) for t in ts)) :
                w[node.name][a][rs] = []

            w[node.name][a][tuple(0 for t in ts)] = [{}]

        continue

    # recursive case
    for a in alpha :            
        for rs in product(*(range(e[t]+1) for t in ts)) :
            w[node.name][a][rs] = W(node, a, rs, debug = True, math = mathmode)

if mathmode :
    sys.exit(0)

# verify
for node in tree.traverse('postorder') :
    print()

    for a in alpha :
        print()

        for rs in product(*(range(e[t]+1) for t in ts)) :
            print(p_dp(node.name, a, rs, numerical = False))
