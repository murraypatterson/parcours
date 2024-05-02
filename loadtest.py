from ete3 import Tree
from networkx.generators.nonisomorphic_trees import nonisomorphic_trees
from itertools import product
import random
import montecarlo_method
import test

ITERATIONS = 6
ALPHABET_SIZE = 5

def constrained_sum_sample_pos(n, total):
    """Return a randomly chosen list of n positive integers summing to total.
    Each such list is equally likely to occur."""

    dividers = sorted(random.sample(range(1, total), n - 1))
    return [a - b for a, b in zip(dividers + [total], [0] + dividers)]

def constrained_sum_sample_nonneg(n, total):
    """Return a randomly chosen list of n nonnegative integers summing to total.
    Each such list is equally likely to occur."""

    return [x - 1 for x in constrained_sum_sample_pos(n, total + n)]

def networkx_to_tree(g, root=1):
    subtrees = {node:Tree(name=node) for node in g.nodes()}
    [*map(lambda edge:subtrees[edge[0]].add_child(subtrees[edge[1]]), g.edges())]
    tree = subtrees[root]
    print(tree.get_ascii())
    return tree

def iterateAlphabet(iterations: int):
    alphabets = []
    for iteration in range(iterations):
        alphabet = [x for x in product(range(iteration + 1), repeat=2) if x[0] != x[1]]
        alphabets.append(alphabet)
    return alphabets

def callMontecarloMethod(tree, alphabet, events):
    analyzer = montecarlo_method.MontecarloMethodTest(tree=tree, transitions=alphabet, events=events)
    return analyzer.getEventsInTree()

def callRecursiveMethod(tree, alphabet, events):
    pass

def main():
    for i in range(2,ITERATIONS):
        trees = nonisomorphic_trees(order=i, create='graph')
        for tree in trees:
            alphabet_with_transitions = {}
            ete_tree = networkx_to_tree(tree)
            alphabets = iterateAlphabet(min(ALPHABET_SIZE, i))
            print(alphabets)
            for alphabet in alphabets:
                if not alphabet:
                    continue
                events = [1] * len(alphabet)
                callMontecarloMethod(ete_tree, alphabet, events)
                

if __name__ == "__main__":
    main()
