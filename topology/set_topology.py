import sys

CPE = "CPE"
LTE = "LTE"
VDSL = "VDSL"
TUNNEL = "TUNNEL"

current_dict = {}
root_level_element_ids = {}
parents_ids = {}

def _get_file_content(file_name):
    with open(file_name, 'r') as f:
        file_content = f.read()
    f.close()
    return file_content


def get_parent_key(curr_id):
    curr_obj = current_dict[curr_id]
    return curr_obj[0]


def get_data():
    raw_data = []
    # parent,type,serial, assetID
    raw_data.append([-1, CPE, 123, 456])
    raw_data.append([123, LTE, 225, 342])
    raw_data.append([123, VDSL, 250, 122])
    raw_data.append([250, TUNNEL, 3448, 12312])
    raw_data.append([250, TUNNEL, 3445, 12312])
    for item in raw_data:
        current_dict[item[2]] = item
        current_id = item[2]
        parent_id = item[0]
        if parent_id == -1:
            root_level_element_ids[current_id] = []
        elif parent_id in parents_ids:
            parents_ids[parent_id].append(current_id)
        elif parent_id in root_level_element_ids:
            root_level_element_ids[parent_id].append(current_id)
        else:
            parents_ids[parent_id] = []
            parents_ids[parent_id].append(current_id)

    for parent_id, kids in root_level_element_ids.items():

        current_type = current_dict[parent_id][1]
        print "{0} ({1})".format(current_type, parent_id)
        for kid in kids:
            current_type = current_dict[kid][1]
            print "  {0} ({1})".format(current_type, kid)
            if kid in parents_ids:
                curr_kid = parents_ids[kid]
                for grand_kid in curr_kid:
                    current_type = current_dict[grand_kid][1]
                    print "    {0} ({1})".format(current_type, grand_kid)


def get_bp_start(prefix, bp_name, suffix):
    #print "{0}: {1}{2}{3}".format("get_bp_start", prefix, bp_name, suffix)
    #print "{0}".format(start_bp_file_name)
    bp_start = _get_file_content("filename")
    print bp_start


def main(argv):
    #for i in range(len(argv)):
    #    print ("argv={0}\n".format(argv[i]))

    #bp_name = argv[1]
    get_data()

if __name__ == '__main__':
    main(sys.argv)
