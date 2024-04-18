from ete3 import Tree
from networkx.generators.nonisomorphic_trees import nonisomorphic_trees
import montecarlo_method
import test

ITERATIONS = 6

def networkx_to_tree(g, root=1):
    subtrees = {node:Tree(name=node) for node in g.nodes()}
    [*map(lambda edge:subtrees[edge[0]].add_child(subtrees[edge[1]]), g.edges())]
    tree = subtrees[root]
    print(tree.get_ascii())
    return tree

def main():
    for i in range(2,ITERATIONS):
        trees = nonisomorphic_trees(order=i, create='graph')
        for tree in trees:
            tree_name = networkx_to_tree(tree)

if __name__ == "__main__":
    main()
