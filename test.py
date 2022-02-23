
import sys
from ete3 import Tree
from itertools import product

def get_alphabet(lines) :

    alpha = set([])

    for line in lines :
        alpha.add(line.strip())

    return sorted(list(alpha))


def get_transitions(alpha) :

    return [(a,b) for a in alpha for b in alpha if b != a]


def project(ts, sigma) :

    p = {}
    p[sigma] = -1 # signifies unlimited
    for r in rs :
        a, b = r

        if a == sigma :
            p[b] = rs[r]

    return p


#def distributions(a, n, p) :

    # all mulitisets from a of size n, under constraints p (a projection)


def non_zero(rs) :

    for r in rs :
        if rs[r] > 0 :
            return False

    return True


def w(u, a, rs, sigma) :

    if u.is_leaf() :
        if non_zero(rs) :
            return []

#    else :


# Main

tree = Tree(sys.argv[1], format = 8)
a = get_alphabet(open(sys.argv[2],'r'))
ts = get_transitions(a)
rs = {t:0 for t in ts}
rs[('a','b')] = 3
rs[('a','c')] = 2

print(tree)
print()
print(a)
print()
print(ts)
print()
print(rs)
print()

p = project(rs, 'a')
print(p)
print()
