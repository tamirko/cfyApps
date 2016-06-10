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

exclude_types_counter = 0
excluded_raw_types = []
current_raw_types = [['Fortigate', 'Vyata'], ['Vyata', 'F5'], ['Fortigate', 'Vyata', 'ODL']]
for current_raw_type in current_raw_types:
    permutations = itertools.permutations(current_raw_type, len(current_raw_type))
    current_list_of_excluded_permutations = list(permutations)
#    print current_list_of_excluded_permutations
    for exclude_permutation in current_list_of_excluded_permutations:
        excluded_raw_types.append(exclude_permutation)
        exclude_types_counter += 1
print "excluded_complex_blueprints_counter {0}".format(exclude_types_counter)
#quit()

for current_node_count in xrange(min_nodes_count, max_nodes_count_p1):
    permutations = itertools.permutations(['Fortigate', 'Vyata', 'ODL', 'Numinum', 'F5'], current_node_count)
    list_of_permutations = list(permutations)
    print "{1} permutations where order matters. -#nodes: {0}".format(current_node_count,len(list_of_permutations))
    print list_of_permutations
    for permutation in list_of_permutations:
        if permutation in excluded_raw_types:
            print "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        #print permutation
        for current_internal_node_count in xrange(1, current_node_count):
            internal_permutations = itertools.permutations(permutation, current_internal_node_count)
            if permutation in excluded_raw_types:
                print "yyyyyyyyyyyyyyyyyyyyyyyyyyyyy"

            list_of_internal_permutations = list(internal_permutations)
#            print list_of_internal_permutations
        #print "-------------------------------------------------------------------------"
    print "-------------------------------------------------------------------------"