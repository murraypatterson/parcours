
import sys
from ete3 import Tree

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

        to = sorted(set(alpha) - set([sigma]))
        p = [rs[(sigma,x)] for x in to]

        for s in bars_and_stars(k-1, n, p) :

            rsp = {r:rs[r] for r in rs}
            for i in range(len(to)-1) :
                rsp[(sigma,to[i])] -= s[i]

            print(s)
            print(rsp)
            


# Main

tree = Tree(sys.argv[1], format = 8)
alpha = get_alphabet(open(sys.argv[2],'r'))
k = len(alpha)
ts = get_transitions(alpha)
rs = {t:0 for t in ts}
rs[('a','b')] = 1
rs[('a','c')] = 0

print(tree)
print()
print(alpha)
print()
print(ts)
print()
print(rs)
print()

ways = w(tree, rs, 'a')
