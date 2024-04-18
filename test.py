
import sys
from ete3 import Tree
from itertools import product
from sympy.utilities.iterables import multiset_permutations
import numpy
import parse

class RecursiveTest:
    # bars and stars with a restriction for each bar --- adapted from:
    # https://stackoverflow.com/questions/28965734/general-bars-and-stars
    def __init__(self, tree_filename=None, alpha=None, events=None, concisemode=False):
        self.tree = Tree(tree_filename, format=8)
        self.alpha = self.get_alphabet(alpha)
        self.ts = self.get_transitions(self.alpha)
        self.k = len(self.alpha)
        self.w = {}
        self.e = self.process_events(events, self.ts)
        self.concisemode = concisemode

    def bars_and_stars(self, bars, stars, restriction = [], prefix = []) :

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
            yield from self.bars_and_stars(bars-1, stars-i, restriction, prefix + [i])

    #
    # produce a multiset from a set a and its multiplicities
    def multi(self, a, ms) :

        s = []
        for x,y in zip(a, ms) :
            s += [x] * y

        return s

    #
    # the \otimes operator of the manuscript (a kind of "cartesian
    # product")
    def otimes(self, S, T) :

        return [{**s, **t} for s in S for t in T]

    #
    # a concise pretty print for an entry of a dictionary, assuming branch
    # (key) is a character, and state transition (value) in binary
    def p_c(self, b, i, j) :

        if i == self.alpha[0] :
            assert j == self.alpha[1]
            return b.upper()

        assert i == self.alpha[1]
        return b.lower()

    #
    # pretty print the entries of a dictionary
    def p_d(self, d, math = False) :

        # an adhoc concise mode for the special case with two states
        if self.concisemode :
            return r'\{' + ', '.join(self.p_c(x,d[x][0],d[x][1]) for x in d) + r'\}'

        if math :
            return r'\{' + ', '.join(r'{}:\text{{{}}}{{\rightarrow}}\text{{{}}}'.format(x,d[x][0],d[x][1]) for x in d) + r'\}'

        return '{' + ', '.join('{}:{}->{}'.format(x,d[x][0],d[x][1]) for x in d) + '}'

    #
    # pretty print a list of dictionaries (an entry w of dp table)
    def p_w(self, w, math = False) :

        s = ', '.join(self.p_d(d, math=math) for d in w)

        if math :
            if not s :
                return r'\0'
            if s == r'\{\}' :
                return r'\1'
            return r'\{' + s + r'\}'

        return '[' + s + ']'

    #
    # print an entry of the dp table (for debugging purposes)
    def p_dp(self, u, sigma, rs, numerical = False, math = False) :

        d = self.w[u][sigma][rs]
        p = self.p_w(d, math = math)
        if numerical :
            p = len(d)

        if math :
            r = ','.join(str(x) for x in rs)
            return r'W_{}({} ~|~ \text{{{}}}) %= {}'.format(u, r, sigma, p)
        return 'w[{}][{}][{}] = {}'.format(u, sigma, rs, p)

    #
    # W_u(r_1, ..., r_m | sigma)
    def W(self, u, sigma, rs, debug = False, prune = False, math = False) :
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

        to = sorted(set(self.alpha) - set([sigma]))
        rsd = {t : r for t,r in zip(self.ts,rs)}
        c = [rsd[(sigma,x)] for x in to]

        # s in S
        for ms in self.bars_and_stars(self.k-1, n, c) :
            s = self.multi(to + [sigma], ms)

            # r_1', ..., r_m'
            rpsd = {t : rsd[t] for t in self.ts}
            for j in range(len(to)) :
                rpsd[(sigma,to[j])] -= ms[j]

            # p_1 in P_V(r_1') ... p_m in P_V(r_m')
            for ps in product(*(self.bars_and_stars(n-1, rpsd[t]) for t in self.ts)) :

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
                        w_v = self.w[v.name][pi[i]][tuple(p[i] for p in ps)]
                        prod = self.otimes(prod, w_v)

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
                                    
                            print(pref, self.p_dp(v.name, pi[i], tuple(p[i] for p in ps), math = math))

                            bsw = True
                            sw = True

                        if prune and not w_v :

                            if debug :
                                print('    ..prune')

                            break

                    if debug :
                        pwb = self.p_w(base, math = math)
                        pwp = self.p_w(prod, math = math)

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

            print('=', self.p_w(result, math=math))
            if math :
                print(r'\end{multline*}')

        return result

    #
    # obtain the alphabet: set of unique substrings from a string
    def get_alphabet(self, string) :

        alpha = []
        for s in string.split() :

            if s not in alpha :
                alpha.append(s)

        return alpha

    #
    # obtain transitions from an alphabet: number of pairs (a,b) where b
    # is different from a
    def get_transitions(self, alpha) :

        return [(a,b) for a in alpha for b in alpha if b != a]

    #
    # obtain (number of) transition events from a string and create a
    # dictionary in the context of a known set of transitions
    def process_events(self, string, ts) :

        e = {t:0 for t in ts}
        for s in string.split() :

            k,a,b = parse.parse('{}:{}->{}', s)
            e[(a,b)] = int(k)

        return e

    def test(self):
        count = 0
        mathmode = False
        if mathmode :
            print()
            print(r'\newcommand{\0}{\emptyset}')
            print(r'\newcommand{\1}{\{\emptyset\}}')
            print(r'\newcommand{\x}{\otimes}')
            print()
            print(r'\begin{comment}')

        print()
        print('tree:', self.tree.get_ascii(show_internal=True))
        print()
        print('alphabet:', self.alpha)
        print()
        print('transitions:', self.ts)
        print()
        print('events:', self.e)
        
        if mathmode :
            print()
            print(r'\end{comment}')

        for node in self.tree.traverse('postorder') :

            self.w[node.name] = {a : numpy.ndarray(shape=tuple(self.e[t]+1 for t in self.ts), dtype=object) for a in self.alpha}

            # base case
            if node.is_leaf() :

                for a in self.alpha :
                    for rs in product(*(range(self.e[t]+1) for t in self.ts)) :
                        self.w[node.name][a][rs] = []

                    self.w[node.name][a][tuple(0 for t in self.ts)] = [{}]

                continue

            # recursive case
            for a in self.alpha :            
                for rs in product(*(range(self.e[t]+1) for t in self.ts)) :
                    self.w[node.name][a][rs] = self.W(node, a, rs, debug = True, math = mathmode)
        for a in self.alpha:
            d = self.W(self.tree.get_tree_root(),a,(1,1,1,1,1,1))
            print("test numeric return")
            print(len(d))
            count += len(d)
            pass
        if mathmode :
            sys.exit(0)

        # verify
        for node in self.tree.traverse('postorder') :
            print()

            for a in self.alpha :
                print()

                for rs in product(*(range(self.e[t]+1) for t in self.ts)) :
                    print(self.p_dp(node.name, a, rs, numerical = False))
        return count
#
# Main
#----------------------------------------------------------------------
if __name__ == "__main__":
    analyzer0 = RecursiveTest()
    analyzer = RecursiveTest(sys.argv[1], sys.argv[2], sys.argv[3])
    print(analyzer.test())
