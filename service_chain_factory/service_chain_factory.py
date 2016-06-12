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

OUTER_PREFIX = "AAA_"
OUTER_SUFFIX = "_AAA"

INTERNAL_DELIM = "_XXX_"


min_tiers_count = 3
max_tiers_count = 4

relevant_blueprints = []


def _get_excluded_blueprints():
    excluded_complex_blueprints_counter = 0
    excluded_raw_blueprints = []
    orig_raw_excluded_blueprints = ServiceChainDictionary.excluded_real_blueprints_combinations
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
    excluded_internal_counter = 0
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
                                #print " --- {0}".format(internal_permutation)
                                current_internal_relevant_permutations.append(internal_permutation)
                            else:
                                excluded_internal_counter +=1

                if use_this_permutation:
                    #print permutation
                    relevant_blueprints.append(permutation)
                    permutation_key = "".join(permutation)
                    all_internal_relevant_permutations[permutation_key] = \
                        copy.deepcopy(current_internal_relevant_permutations)
                    actual_permutations_counter += 1
                else:
                    excluded_permutations_counter += 1
                #print "---------------------------------------------------------------------------------------------------"
            else:
                excluded_permutations_counter += 1
        #print "---------------------------------------------------------------------------------------------------"
    print "Maximum {1} permutations where order matters. -#blueprints: {0}". \
            format(current_blueprints_count, total_permutations_counter)
    print "Excluded permutations {0}".format(excluded_permutations_counter)
    print "Actual permutations {0}".format(actual_permutations_counter)
    print "Excluded internals {0}".format(excluded_internal_counter)
    print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    return relevant_blueprints, all_internal_relevant_permutations, actual_permutations_counter, \
           excluded_internal_counter


def are_all_parts_in(current_perm, curr_combination, curr_combination_len):
    parts_in_counter = 0
    for curr_part in curr_combination:
        tuple_curr_part = (curr_part,)
        if tuple_curr_part in current_perm:
            parts_in_counter += 1
    #print parts_in_counter, curr_combination_len
    return parts_in_counter == curr_combination_len


def is_there_circle(current_perm, curr_perm_str, curr_combination, curr_combination_len):
    print "is_there_circle"
    for curr_node_template in current_perm:
        if curr_node_template[::-1] not in current_perm:
            print "reverse not in current_perm"
            quit()

    return False


def is_there_a_contradiction(current_perm, curr_perm_str, curr_combination, curr_combination_len):
    print "is_there_a_contradiction"
    parts_in_counter = 0
    for curr_part in curr_combination:
        if curr_part in current_perm:
            parts_in_counter += 1

    return parts_in_counter == curr_combination_len


def iterate_over_current_permutation(current_perm, list_permutations, curr_combination, curr_combination_str, curr_combination_len):
    #print "   +++ {0}".format(list_permutations)
    joint_perm = ""
    for curr_node_template in current_perm:
        print "    ++++ {0}".format(curr_node_template)
        curr_node_template_str = INTERNAL_DELIM.join(curr_node_template)
        joint_perm += "{0}{1}".format(curr_node_template_str, INTERNAL_DELIM)
    joint_perm = joint_perm[:-1]
    curr_perm_str = "{0}{1}{2}".format(OUTER_PREFIX, joint_perm, OUTER_SUFFIX)
    if are_all_parts_in(list(current_perm), curr_combination, curr_combination_len):
        print "xxxxx b4 is_there_a_contradiction"
        quit()
        if is_there_a_contradiction(current_perm, curr_perm_str, curr_combination, curr_combination_len):
            return
        print "xxxxx b4 is_there_circle"
        if is_there_circle(current_perm, curr_perm_str, curr_combination, curr_combination_len):
            return

    if len(current_perm) > 3:
        quit()


def iterate_over_combinations():
    current_relevant_combinations, all_internal_relevant_permutations, current_permutations_counter, \
        excluded_internal_counter = get_relevant_combinations()
    if current_permutations_counter != len(current_relevant_combinations):
        print "Error: Wrong number of blueprints {0}".format(current_permutations_counter)
        quit()

    for curr_combination in current_relevant_combinations:
        print "Current combination: {0}".format(curr_combination)
        permutation_key = "".join(curr_combination)
        current_internal_combinations = all_internal_relevant_permutations[permutation_key]
        print "  Current internal combinations {0}:".format(len(current_internal_combinations))
        #for current_keys in current_internal_combinations:
        #    print "  +{0}".format(current_keys)
        #print "---------------------------"
        curr_combination_str = "{0}{1}{2}".format(OUTER_PREFIX, INTERNAL_DELIM.join(curr_combination), OUTER_SUFFIX)
        curr_combination_len = len(curr_combination)
        for current_internal_combinations_count in xrange(2, len(current_internal_combinations)):
            permutations = itertools.permutations(current_internal_combinations, current_internal_combinations_count)
            list_permutations = list(permutations)
            print "  Iterating over {0} permutations:".format(len(list_permutations))
            for current_perm in list_permutations:
                if 'PaloAxlto' not in curr_combination_str:
                    print "  curr_combination_str {0}".format(curr_combination_str)
                    print "  curr_combination {0}".format(curr_combination)
                    print "  ++ current_perm {0}".format(current_perm)
                    iterate_over_current_permutation(current_perm, list_permutations, curr_combination, curr_combination_str, curr_combination_len)
                #quit()
            #quit()



def main(argv):
    for i in range(len(argv)):
        print ("argv{0}={1}\n".format(i, argv[i]))

    iterate_over_combinations()


if __name__ == '__main__':
    main(sys.argv)
