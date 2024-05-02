from ete3 import Tree
from networkx.generators.nonisomorphic_trees import nonisomorphic_trees
from itertools import product
import montecarlo_method
import test

ITERATIONS = 6

def networkx_to_tree(g, root=1):
    subtrees = {node:Tree(name=node) for node in g.nodes()}
    [*map(lambda edge:subtrees[edge[0]].add_child(subtrees[edge[1]]), g.edges())]
    tree = subtrees[root]
    print(tree.get_ascii())
    return tree

def iterateAlphabet(iterations: int, tree: Tree):
    alphabets = []
    for iteration in range(iterations):
        alphabet = [x for x in product(range(iteration + 1), repeat=2) if x[0] != x[1]]
        alphabets.append(alphabet)
    return alphabets

def main():
    for i in range(2,ITERATIONS):
        trees = nonisomorphic_trees(order=i, create='graph')
        for tree in trees:
            tree_name = networkx_to_tree(tree)
    print(str(iterateAlphabet(3, "")))

if __name__ == "__main__":
    main()
