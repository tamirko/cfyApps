import os

import itertools

# order matters :
#permutations = itertools.permutations([1,2,3,4], 2)
#print list(permutations)
#print "--------------------------------------------------"
# order DOES NOT matter :
#print list(itertools.combinations('123', 2))


min_nodes_count = 2
max_nodes_count_p1 = 6

for current_node_count in xrange(min_nodes_count, max_nodes_count_p1):

    permutations = itertools.permutations(['AAA', 'BBB', 'CCC', 'DDD', 'EEE'], current_node_count)
    list_of_permutations = list(permutations)
    print "{1} permutations where order matters. -#nodes: {0}".format(current_node_count,len(list_of_permutations))
    #print list_of_permutations
    for permutation in list_of_permutations:
        print permutation
        for current_internal_node_count in xrange(1, current_node_count):
            internal_permutations = itertools.permutations(permutation, current_internal_node_count)
            list_of_internal_permutations = list(internal_permutations)
            print list_of_internal_permutations
        print "-------------------------------------------------------------------------"
    print "-------------------------------------------------------------------------"