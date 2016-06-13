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


min_tiers_count = 2
max_tiers_count = 4

relevant_blueprints = []
main_combinations_map = {}
all_permutations = []


def _get_excluded_blueprints_sets():
    excluded_complex_blueprints_sets_counter = 0
    excluded_raw_blueprints_sets = []
    orig_raw_excluded_blueprints_sets = ServiceChainDictionary.excluded_real_blueprints_sets
    for current_raw_excluded_blueprint_set in orig_raw_excluded_blueprints_sets:
        permutations = itertools.permutations(current_raw_excluded_blueprint_set, len(current_raw_excluded_blueprint_set))
        current_list_of_excluded_permutations = list(permutations)
        for exclude_permutation in current_list_of_excluded_permutations:
            excluded_raw_blueprints_sets.append(exclude_permutation)
            excluded_complex_blueprints_sets_counter += 1
    print "Excluded complex blueprints sets: {0}".format(excluded_complex_blueprints_sets_counter)
    return excluded_raw_blueprints_sets


def should_b_included(combination, excluded_raw_blueprints_sets, orig_excluded_relationships, current_blueprints_count):
    if combination not in excluded_raw_blueprints_sets:
        combination_str = "".join(combination)
        sorted_combination_str = "".join(sorted(combination))
        for excluded_raw_blueprint_set in excluded_raw_blueprints_sets:
            #print "excluded_raw_blueprint_set {0}".format(excluded_raw_blueprint_set)
            sorted_excluded_raw_blueprint_set_str = "".join(sorted(excluded_raw_blueprint_set))
            if sorted_excluded_raw_blueprint_set_str in sorted_combination_str:
                #print "xxxxxx111 {0}".format(combination_str)
                return False

            all_excluded_are_included_in_combination = True
            excluded_raw_blueprint_set_list = list(excluded_raw_blueprint_set)
            for raw_blueprint_part in excluded_raw_blueprint_set_list:
                if raw_blueprint_part not in combination:
                    all_excluded_are_included_in_combination = False
                    break

            if all_excluded_are_included_in_combination:
                #print "xxxxxx22 {0}".format(combination_str)
                return False

    return True


def get_main_combinations():
    excluded_combinations_counter = 0
    orig_excluded_relationships = ServiceChainDictionary.excluded_relationships
    excluded_raw_blueprints_sets = _get_excluded_blueprints_sets()
    print "Excluded real blueprints sets:"
    for curr_set in excluded_raw_blueprints_sets:
        print " {0}".format(curr_set)
    total_combinations_counter = 0
    actual_combinations_counter = 0
    for current_blueprints_count in range(min_tiers_count, max_tiers_count):
        blueprints_combinations = itertools.combinations(ServiceChainDictionary.blueprints_real_names, current_blueprints_count)
        list_of_blueprints_combinations = list(blueprints_combinations)
        total_combinations_counter += len(list_of_blueprints_combinations)
        for blueprint_combination in list_of_blueprints_combinations:
            include_it = should_b_included(blueprint_combination,
                excluded_raw_blueprints_sets, orig_excluded_relationships, current_blueprints_count)

            if include_it:
                combination_key = "".join(blueprint_combination)

                if not main_combinations_map.has_key(combination_key):
                    main_combinations_map[combination_key] = blueprint_combination
                actual_combinations_counter += 1
            else:
                excluded_combinations_counter += 1
        #print "---------------------------------------------------------------------------------------------------"
    print "Maximum {1} combinations where order does NOT matter. -#blueprints: {0}". \
            format(current_blueprints_count, total_combinations_counter)
    print "Excluded combinations: {0}".format(excluded_combinations_counter)
    print "Actual combinations: {0}".format(actual_combinations_counter)
    print "+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
    return actual_combinations_counter


def are_all_parts_in(current_perm, curr_combination, curr_combination_len):
    parts_in_counter = 0
    for curr_part in curr_combination:
        tuple_curr_part = (curr_part,)
        if tuple_curr_part in current_perm:
            parts_in_counter += 1
    #print parts_in_counter, curr_combination_len
    return parts_in_counter == curr_combination_len


def is_there_circle(current_perm, curr_perm_str, curr_combination, curr_combination_len):
    for curr_node_template in current_perm:
        if curr_node_template[::-1] in current_perm:
            #print "    reverse in current_perm"
            #return True
            #quit()
            break

    return False


def is_there_a_contradiction(current_perm, curr_perm_str, curr_combination, curr_combination_len):
    #print "is_there_a_contradiction"

    #for curr_part in curr_combination:
    #    if curr_part in current_perm:
    #        parts_in_counter += 1

    return False


def iterate_over_current_permutation(current_perm, list_permutations, curr_combination, curr_combination_str, curr_combination_len):
    #print "   +++ {0}".format(list_permutations)
    joint_perm = ""
    for curr_node_template in current_perm:
        #print "    ++++ {0}".format(curr_node_template)
        curr_node_template_str = INTERNAL_DELIM.join(curr_node_template)
        joint_perm += "{0}{1}".format(curr_node_template_str, INTERNAL_DELIM)
    joint_perm = joint_perm[:-1]
    curr_perm_str = "{0}{1}{2}".format(OUTER_PREFIX, joint_perm, OUTER_SUFFIX)
    if are_all_parts_in(list(current_perm), curr_combination, curr_combination_len):
        if is_there_a_contradiction(current_perm, curr_perm_str, curr_combination, curr_combination_len):
            return

        if is_there_circle(current_perm, curr_perm_str, curr_combination, curr_combination_len):
            return

        #print "   ++ current_perm {0}".format(current_perm)
    #else:
    #    print "    not all parts are in xxxxxxxxxxx"

    if len(current_perm) > 664:
        quit()


def digest_main_combination(combination_key, combination_len, curr_combination):
    max_length = len(curr_combination)
    combination_list = []
    for curr_length in range(1, max_length+1):
        permutations = itertools.permutations(curr_combination, curr_length)
        current_list_of_permutations = list(permutations)
        for permutation in current_list_of_permutations:
            combination_list.append(permutation)

    curr_permutations = []
    for curr_len in range(2, combination_len):
        all_permutation_of_curr_combination = itertools.permutations(combination_list, curr_len)
        for permutation in all_permutation_of_curr_combination:
            #print "{0}: {1}".format(curr_len, permutation)
            curr_permutations.append(permutation)

    all_permutations.append(curr_permutations)
    return curr_permutations


def filer_out_permutation(combination_key, curr_permutations):
    #print "combination_key: {0}".format(combination_key)
    if len(curr_permutations) < 4:
        print "combination_key: {0}".format(combination_key)
        print "  less than 4"
    elif 1==2:
        for x in curr_permutations:
            print x
        print "++++++++++++++++++++"


def iterate_over_combinations():
    actual_combinations_counter = get_main_combinations()
    if actual_combinations_counter != len(main_combinations_map):
        print "Error: Wrong number of blueprints {0}".format(actual_combinations_counter)
        quit()

    for combination_key in main_combinations_map.keys():
        curr_combination = main_combinations_map[combination_key]
        #print "{0}: {1}".format(combination_key, curr_combination)
        curr_permutations = digest_main_combination(combination_key, len(curr_combination), curr_combination)
        filer_out_permutation(combination_key, curr_permutations)

def main(argv):
    for i in range(len(argv)):
        print ("argv{0}={1}\n".format(i, argv[i]))

    iterate_over_combinations()


if __name__ == '__main__':
    main(sys.argv)
