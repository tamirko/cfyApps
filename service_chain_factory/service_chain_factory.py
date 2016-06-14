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
max_tiers_count = 8

relevant_blueprints = []
main_combinations_map = {}
all_permutations = []

all_permutations_map = {}
excluded_complex_blueprints_sets_counter = 0

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
    for current_blueprints_count in range(min_tiers_count, max_tiers_count+1):
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


def are_all_parts_in(combination_key, current_perm, curr_combination, curr_combination_len):
    parts_in_counter = 0
    for curr_part in curr_combination:
        tuple_curr_part = (curr_part,)
        if tuple_curr_part in current_perm:
            parts_in_counter += 1
        else:
            for curr_sub_perm in current_perm:
                if tuple_curr_part in curr_sub_perm:
                    parts_in_counter += 1
                else:
                    for curr_elem in curr_sub_perm:
                        if tuple_curr_part[0] == curr_elem:
                            parts_in_counter += 1

    #    print "xxx Removing {0} for {1}".format(current_perm, combination_key)
    return parts_in_counter == curr_combination_len


def there_is_no_redundancy(combination_key, current_perm, curr_combination, curr_combination_len):
    for curr_sub_perm1 in current_perm:
        if len(curr_sub_perm1) == 1:
            for curr_sub_perm2 in current_perm:
                if len(curr_sub_perm2) != 1:
                    if curr_sub_perm1 in curr_sub_perm2:
                        #print "xxxx combination_key {0} 1:x {1}:{2}".format(combination_key, curr_sub_perm1, curr_sub_perm2)
                        return False
                    if curr_sub_perm1[0] in curr_sub_perm2:
                        return False
    return True


def is_there_circle(current_perm, curr_perm_str, curr_combination, curr_combination_len):
    for curr_node_template in current_perm:
        if curr_node_template[::-1] in current_perm:
            #print "    reverse in current_perm"
            #return True
            #quit()
            break

    return False


def digest_main_combination(combination_key, combination_len, curr_combination):
    combination_list = []
    combination_len_p1 = combination_len+1
    for curr_length in range(1, combination_len_p1):
        permutations = itertools.permutations(curr_combination, curr_length)
        current_list_of_permutations = list(permutations)
        for permutation in current_list_of_permutations:
            combination_list.append(permutation)

    curr_permutations = []
    for curr_len in range(2, max(3, combination_len_p1)):
        all_permutation_of_curr_combination = itertools.permutations(combination_list, curr_len)
        for permutation in all_permutation_of_curr_combination:
            curr_permutations.append(permutation)

    all_permutations.append(curr_permutations)
    return curr_permutations


def get_permutation_key(curr_perm, get_reversed=False):
    if get_reversed:
        perm = curr_perm
    else:
        perm = curr_perm[::-1]
    curr_key_raw = str(perm).strip('[]')
    curr_key = curr_key_raw.replace(',', '')
    return curr_key


def permutation_doesnt_exist(curr_perm, check_reversed=True):
    curr_key = get_permutation_key(curr_perm)
    if curr_key in all_permutations_map:
        if check_reversed:
            reversed_key = get_permutation_key(curr_perm)
            return reversed_key not in all_permutations_map
        else:
            return True

    if check_reversed:
        reversed_key = get_permutation_key(curr_perm)
        return reversed_key not in all_permutations_map


def add_permutation_to_map(curr_perm, add_reversed=True):
    curr_key = get_permutation_key(curr_perm)
    all_permutations_map[curr_key] = curr_perm
    if add_reversed:
        reversed_key = get_permutation_key(curr_perm, True)
        all_permutations_map[reversed_key] = curr_perm


def filer_out_permutation(combination_key, curr_permutations, curr_combination, combination_len):
    print "combination_key: {0}".format(combination_key)
    for curr_perm in curr_permutations:
        if are_all_parts_in(combination_key, curr_perm, curr_combination, combination_len):
            if there_is_no_redundancy(combination_key, curr_perm, curr_combination, combination_len):
                if permutation_doesnt_exist(curr_perm):
                    add_permutation_to_map(curr_perm)
                    print "    {0}".format(curr_perm)

    #print "++++++++++++++++++++"


def iterate_over_combinations():
    actual_combinations_counter = get_main_combinations()
    if actual_combinations_counter != len(main_combinations_map):
        print "Error: Wrong number of blueprints {0}".format(actual_combinations_counter)
        quit()

    for combination_key in main_combinations_map.keys():
        curr_combination = main_combinations_map[combination_key]
        print "------------------"
        #print "curr_combination {0}: {1}".format(combination_key, curr_combination)
        combination_len = len(curr_combination)
        curr_permutations = digest_main_combination(combination_key, combination_len, curr_combination)
        filer_out_permutation(combination_key, curr_permutations, curr_combination, combination_len)

    print "\n"
    print "max tiers : {0}, permutations {1}".format(max_tiers_count, len(all_permutations_map))

def main(argv):
    for i in range(len(argv)):
        print ("argv{0}={1}\n".format(i, argv[i]))

    iterate_over_combinations()


if __name__ == '__main__':
    main(sys.argv)
