import os

import itertools
import sys
import copy
import ServiceChainDictionary


# order matters :
#permutations = itertools.permutations([1,2,3,4], 2)
#print list(permutations)
#print "--------------------------------------------------"
# order DOES NOT matter :
#print list(itertools.combinations('123', 2))


# Vyata : Router
# FortiGate :FW
# Nominum : DNS server
# PaloAlto : FW
# CSR : Router (Cisco)
# VTM : LB (Brocade)

min_tiers_count = 3
max_tiers_count = 4

relevant_blueprints = []


def _get_excluded_blueprints():
    excluded_complex_blueprints_counter = 0
    excluded_raw_blueprints = []
    orig_raw_excluded_blueprints = ServiceChainDictionary.excluded_real_blueprints
    for current_raw_excluded_blueprint in orig_raw_excluded_blueprints:
        permutations = itertools.permutations(current_raw_excluded_blueprint, len(current_raw_excluded_blueprint))
        current_list_of_excluded_permutations = list(permutations)
        for exclude_permutation in current_list_of_excluded_permutations:
            excluded_raw_blueprints.append(exclude_permutation)
            excluded_complex_blueprints_counter += 1
    print "Excluded complex blueprints {0}".format(excluded_complex_blueprints_counter)
    return excluded_raw_blueprints


def get_relevant_combinations():
    excluded_permutations_counter = 0
    orig_excluded_relationships = ServiceChainDictionary.excluded_relationships
    excluded_raw_blueprints = _get_excluded_blueprints()
    total_permutations_counter = 0
    actual_permutations_counter = 0
    all_internal_relevant_permutations = {}
    for current_blueprints_count in xrange(min_tiers_count, max_tiers_count):
        permutations = itertools.permutations(ServiceChainDictionary.blueprints_real_names, current_blueprints_count)
        list_of_permutations = list(permutations)
        total_permutations_counter += len(list_of_permutations)
        for permutation in list_of_permutations:
            current_internal_relevant_permutations = []

            if permutation not in excluded_raw_blueprints:
                use_this_permutation = True
                for excluded_raw_blueprint in excluded_raw_blueprints:
                    if "".join(excluded_raw_blueprint) in "".join(permutation):
                        use_this_permutation = False
                        break
                for current_excluded_relationship in orig_excluded_relationships:
                    if "".join(current_excluded_relationship) in "".join(permutation):
                        use_this_permutation = False
                        break
                if use_this_permutation:
                    for current_internal_node_count in xrange(1, current_blueprints_count):
                        internal_permutations = itertools.permutations(permutation, current_internal_node_count)
                        for internal_permutation in list(internal_permutations):
                            if internal_permutation not in excluded_raw_blueprints:
                                use_this_permutation = True
                                for excluded_raw_blueprint in excluded_raw_blueprints:
                                    if "".join(excluded_raw_blueprint) in "".join(internal_permutation):
                                        use_this_permutation = False
                                        break
                            if use_this_permutation:
                                for current_excluded_relationship in orig_excluded_relationships:
                                    if "".join(current_excluded_relationship) in "".join(internal_permutation):
                                        use_this_permutation = False
                                        break

                            if use_this_permutation:
                                print " --- {0}".format(internal_permutation)
                                current_internal_relevant_permutations.append(internal_permutation)

                if use_this_permutation:
                    print permutation
                    relevant_blueprints.append(permutation)
                    permutation_key = "".join(permutation)
                    all_internal_relevant_permutations[permutation_key] = \
                        copy.deepcopy(current_internal_relevant_permutations)
                    actual_permutations_counter += 1
                else:
                    excluded_permutations_counter += 1
                print "---------------------------------------------------------------------------------------------------"
            else:
                excluded_permutations_counter += 1
        print "---------------------------------------------------------------------------------------------------"
    print "Maximum {1} permutations where order matters. -#blueprints: {0}". \
            format(current_blueprints_count, total_permutations_counter)
    print "Excluded permutations {0}".format(excluded_permutations_counter)
    print "Actual permutations {0}".format(actual_permutations_counter)
    return relevant_blueprints, all_internal_relevant_permutations, actual_permutations_counter


def main(argv):
    for i in range(len(argv)):
        print ("argv{0}={1}\n".format(i, argv[i]))

    current_relevant_combinations, all_internal_relevant_permutations, current_permutations_counter = \
        get_relevant_combinations()
    if current_permutations_counter != len(current_relevant_combinations):
        print "Error: Wrong number of blueprints {0}".format(current_permutations_counter)
        quit()

    for curr_combination in current_relevant_combinations:
        #print curr_combination
        permutation_key = "".join(curr_combination)
        current_internal_combinations =all_internal_relevant_permutations[permutation_key]
        #for current_keys in current_internal_combinations:
        #    print " +{0}".format(current_keys)
        #print "---------------------------"

if __name__ == '__main__':
    main(sys.argv)
