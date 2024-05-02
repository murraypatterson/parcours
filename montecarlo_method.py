from ete3 import Tree
from sympy.utilities.iterables import multiset_permutations
from collections import deque
import random

class MontecarloMethodTest:
    def __init__(self, tree, transitions, events, sampleSize=50000):
        self.tree = tree
        self.transitions = transitions
        self.events = events
        self.sampleSize = sampleSize

    def multi(self, a, ms):
        s = []
        for x, y in zip(a, ms):
            s += [x] * y
        return s

    def getTotalPermutationsGeneralized(self):
        s = [x for x in self.transitions]
        s.append("None")
        multiSet = self.multi(s, [*self.events, len(list(self.tree.traverse())) - sum(self.events) - 1])
        permutations = list(multiset_permutations(multiSet))
        permutations_with_root = []
        for permutation in permutations:
            deck = deque(permutation)
            deck.appendleft("None")
            permwithroot = list(deck)
            permutations_with_root.append(permwithroot)
        return permutations_with_root

    def generateRandomTree(self, permutations):
        permutation = random.choice(permutations)
        for index, node in enumerate(self.tree.traverse("preorder")):
            node.add_feature("mutation", permutation[index])
            node.add_feature("value", None)
        return self.tree, permutation

    def findTransitionNodes(self):
        matches = []
        for n in self.tree.traverse():
            if n.mutation in self.transitions:
                matches.append(n)
        return matches

    def checkValidTreeGeneral(self):
        events = self.findTransitionNodes()
        for event in events:
            current_mutation = event.mutation
            while event.up is not None:
                ancestor = event.up
                if ancestor.mutation == "None":
                    if ancestor.value is None:
                        ancestor.add_feature("value", current_mutation[0])
                    elif ancestor.value != current_mutation[0]:
                        return False               
                if ancestor.mutation != "None":
                    if ancestor.mutation[1] != current_mutation[0]:
                        return False
                    current_mutation = ancestor.mutation
                event = ancestor
        return True

    def countValidTreesInSampleSizeGeneralized(self, sampleSize, totalPermutations):
        attempts = 0
        count = 0
        previouslyComputed = {}
        for _ in range(sampleSize):
            sampleTree, samplePermutation = self.generateRandomTree(totalPermutations)
            if str(samplePermutation) not in previouslyComputed:
                attempts += 1
                previouslyComputed[str(samplePermutation)] = self.checkValidTreeGeneral()
                if previouslyComputed[str(samplePermutation)]:
                    count += 1
        return count, attempts

    def getEventsInTree(self):
        n = len(list(self.tree.traverse()))
        g = self.getTotalPermutationsGeneralized()
        count, sampleSize2 = self.countValidTreesInSampleSizeGeneralized(self.sampleSize, g)
        estimated_gains_losses = len(g) * (count / sampleSize2)
        print(f"Estimated number of ways to have the given number of events in the tree: {estimated_gains_losses}")

def main():
    TREE_FILE = 'tree.nh'
    TRANSITIONS = [(0,1), (1,0), (1,2), (2,1), (0,2), (2,0)]
    EVENTS = [1, 1, 1, 1, 1, 1]
    SAMPLE_SIZE = 50000

    analyzer = MontecarloMethodTest(Tree(TREE_FILE, format=8), TRANSITIONS, EVENTS, SAMPLE_SIZE)
    analyzer.getEventsInTree()

if __name__ == "__main__":
    main()
