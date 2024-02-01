from ete3 import Tree
from sympy.utilities.iterables import multiset_permutations
from collections import deque
import random
import math

#hardcoding these values for now
TREE_FILE = 'test.nh'
TRANSITIONS = [(0,1),(1,0)]
EVENTS = [2,2]
GAINS = 2
LOSSES = 2
SAMPLE_SIZE = 10000
t = Tree(TREE_FILE, format=8)

# produce a multiset from a set a and its multiplicities
def multi(a, ms) :

    s = []
    for x,y in zip(a, ms) :
        s += [x] * y

    return s

def getTotalPermutationsGeneralized(n):
    s = [x for x in TRANSITIONS]
    s.append("None")
    multiSet = multi(s, [*EVENTS, n-sum(EVENTS)-1])
    permutations = list(multiset_permutations(multiSet))
    # We initially ignored the root node, now we're adding it back. TODO: find a cleaner way to do this
    permutations_with_root = []
    for permutation in permutations:
        deck = deque(permutation)
        deck.appendleft("None")
        permwithroot = list(deck)
        permutations_with_root.append(permwithroot)
    return(permutations_with_root)

def getTotalPermutations(g,l,n):
    s = ["G","L","N"]
    multiSet = multi(s,[GAINS,LOSSES,n-(GAINS+LOSSES)-1])
    print("multiset: {}".format(s))
    permutations = list(multiset_permutations(multiSet))
    # We initially ignored the root node, now we're adding it back. TODO: find a cleaner way to do this
    permutations_with_root = []
    for permutation in permutations:
        deck = deque(permutation)
        deck.appendleft("N")
        permwithroot = list(deck)
        permutations_with_root.append(permwithroot)
    return(permutations_with_root)

def generateRandomTree(t:Tree, permutations:list):
    permutation = random.choice(permutations)
    for index, node in enumerate(t.traverse("preorder")):
        node.add_feature("mutation",permutation[index])
        node.add_feature("value", None)
    return t, permutation

def findTransitionNodes(t:Tree):
    matches = []
    for n in t.traverse():
        if n.mutation in TRANSITIONS:
            matches.append(n)
    return matches

def checkValidTreeGeneral(t:Tree):
    # TODO: this function
    print(t.get_ascii(show_internal=True, attributes=["mutation"]))
    events = findTransitionNodes(t)
    for event in events:
        current_mutation = event.mutation
        while event.up is not None:
            ancestor = event.up
            if ancestor.mutation == "None":
                if ancestor.value is None:
                    ancestor.add_feature("value", current_mutation[0])
                elif ancestor.value != current_mutation[0]:
                    return False               
            if ancestor.mutation !="None":
                if ancestor.mutation[1] != current_mutation[0]:
                    return False
                current_mutation = ancestor.mutation
            event = ancestor
    return True
           
def checkValidTree(t:Tree):
    r = t.get_tree_root
    gain_events = t.search_nodes(mutation="G")
    loss_events = t.search_nodes(mutation="L")
    print(t.get_ascii(show_internal=True, attributes=["mutation"]))
    if not gain_events and not loss_events:
        return None
    for event in gain_events+loss_events:
        # Check for collisions above
        current_mutation = event.mutation
        while event.up is not None:
            ancestor = event.up
            if current_mutation == "G":
                if(ancestor.mutation == 'G'):
                    return False
                if(ancestor.value is None):
                    ancestor.add_feature("value", 0)
                elif(ancestor.value == 1 and ancestor.mutation != "L"):
                    return False
            elif current_mutation == "L":
                if(ancestor.mutation == 'L'):
                    return False
                if(ancestor.value is None):
                    ancestor.add_feature("value", 1)
                elif(ancestor.value == 0 and ancestor.mutation != "G"):
                    return False
            if(ancestor.mutation != "N"):
                current_mutation = ancestor.mutation
            event = ancestor
    return True
        
def isValidTree(t:Tree):
    # Traverse from all the leaves to the root. If there are ever two gains or two losses in a row, then it is not a valid tree
    validTree = True
    for leafNode in t.get_leaves():
        l = [node.mutation for node in  leafNode.iter_ancestors() if node.mutation != "N"]
        if not any(l):
            validTree = True
        elif consecutiveDuplicates(l):
            validTree = False
            break
        # If there is a loss without a gain before, then it's not a valid tree as well
        elif l[0] == 'L':
            validTree = False
            break
    return validTree

def consecutiveDuplicates(l):
    for i in range (len(l) - 1):
        if l[i] == l[i + 1]:
            return True
    return False


def countValidTreesInSampleSize(sampleSize, totalPermutations, tree):
    attempts = 0
    count = 0
    previouslyComputed = dict()
    for i in range(sampleSize):
        sampleTree, samplePermutation = generateRandomTree(tree, totalPermutations)
        if str(samplePermutation) not in previouslyComputed:
            attempts += 1
            previouslyComputed[str(samplePermutation)] = checkValidTree(sampleTree)
            print(previouslyComputed[str(samplePermutation)])
            if previouslyComputed[str(samplePermutation)]:
                count += 1
    
    return count, attempts

def countValidTreesInSampleSizeGeneralized(sampleSize, totalPermutations, tree):
    attempts = 0
    count = 0
    previouslyComputed = dict()
    for i in range(sampleSize):
        sampleTree, samplePermutation = generateRandomTree(tree, totalPermutations)
        if str(samplePermutation) not in previouslyComputed:
            attempts += 1
            previouslyComputed[str(samplePermutation)] = checkValidTreeGeneral(sampleTree)
            print(previouslyComputed[str(samplePermutation)])
            if previouslyComputed[str(samplePermutation)]:
                count += 1
    
    return count, attempts

n = len(list(t.traverse()))
p = getTotalPermutations(GAINS,LOSSES,n)

if(GAINS+LOSSES == 0):
    raise Exception("Can not have zero gains and zero losses")

count, sampleSize = countValidTreesInSampleSize(SAMPLE_SIZE, p, t)
estimated_gains_losses = len(p) * (count / sampleSize)

g = getTotalPermutationsGeneralized(n)

print("nodes on tree excluding root: {}".format(n-1))
print("number of possible trees: {}".format(len(p)))
print("valid trees found: {}".format(count))
print("attempts: {}".format(sampleSize))
print(estimated_gains_losses)

print("----------------GENERALIZED VERSION----------------------")
count2, sampleSize2 = countValidTreesInSampleSizeGeneralized(SAMPLE_SIZE, g, t)
estimated_gains_losses2 = len(g) * (count2 / sampleSize2)
print(f"number of total possible trees: {len(g)}")
print(f"valid trees found: {count2}")
print(f"attempts: {sampleSize2}")
print(f"estimated number of ways to have the given number of events in the tree {estimated_gains_losses2}")

 
