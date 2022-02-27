
import sys
from ete3 import Tree

#
# obtain the alphabet: set of unique string from a set of lines
def get_alphabet(lines) :

    alpha = set([])

    for line in lines :
        alpha.add(line.strip())

    return sorted(list(alpha))

#
# obtain transitions from an alphabet: number of pairs (a,b) where b
# is different from a
def get_transitions(alpha) :

    return [(a,b) for a in alpha for b in alpha if b != a]

#
# project a counts dictionary down to a source sigma: keep track of
# only those counts which originate from sigma.  Note that this is
# effectively a dictionary from the alphabet to positive integers
def project(rs, sigma) :

    p = {}
    for r in rs :
        a, b = r

        if a == sigma :
            p[b] = rs[r]

    return p

#
# bars and stars with a restriction for each bar --- adapted from:
# https://stackoverflow.com/questions/28965734/general-bars-and-stars
def bars_and_stars(bars, stars, restriction, prefix = []) :

    if stars == 0 :
        yield prefix + [0]*(bars+1)
        return

    if bars == 0 :
        yield prefix + [stars]
        return

    for i in range(min(restriction[len(prefix)]+1, stars+1)) :
        yield from bars_and_stars(bars-1, stars-i, restriction, prefix + [i])

#
# if any element of counts dictionary rs is non-zero
def non_zero(rs) :

    for r in rs :
        if rs[r] > 0 :
            return False

    return True

#
# W_u(r_1, ..., r_m | sigma)
def w(u, rs, sigma) :

    if u.is_leaf() :
        if non_zero(rs) :
            return []

    else :
        v = u.children
        n = len(v)

        p = project(rs, sigma)
        restriction = [p[x] for x in sorted(p)]
        
        for s in bars_and_stars(k-1, n, restriction) :
            print(s)

# Main

tree = Tree(sys.argv[1], format = 8)
a = get_alphabet(open(sys.argv[2],'r'))
k = len(a)
ts = get_transitions(a)
rs = {t:0 for t in ts}
rs[('a','b')] = 1
rs[('a','c')] = 0

print(tree)
print()
print(a)
print()
print(ts)
print()
print(rs)
print()

ways = w(tree, rs, 'a')
