import sys

start_bp_file_name = "bp_start.yaml"
inputs_section_file_name = "inputs_section.yaml"
node_types_file_name = "node_types.yaml"
node_templates_file_name = "node_templates.yaml"
branch_file_name = "branch.yaml"
end_bp_file_name = "bp_end.yaml"

excluded_node_template_elements = ["type:", "interfaces:", "relationships:"]
branches_inputs = []
bp_inputs_to_be_removed = []


def _get_file_content(file_name):
    with open(file_name, 'r') as f:
        file_content = f.read()
    f.close()
    return file_content


def get_bp_start(prefix, bp_name, suffix):
    bp_start = _get_file_content(start_bp_file_name)
    return bp_start


def get_bp_branch_inputs():
    input_lines = []
    for curr_input in branches_inputs:
        input_lines.append("  {0}: ".format(curr_input))
        input_lines.append("    default: \"\"")
    return input_lines


def get_other_inputs():
    inputs_section = _get_file_content(inputs_section_file_name)
    other_inputs_lines = inputs_section.splitlines()
    inputs_lines = []
    for curr_input_line in other_inputs_lines:
        clean_line = curr_input_line.lstrip().strip().split(":")
        input_name = clean_line[0].lstrip().strip()
        if "{0}:".format(input_name) not in bp_inputs_to_be_removed:
            inputs_lines.append(curr_input_line)

    return inputs_lines


def get_bp_inputs():
    input_lines = get_other_inputs()
    return input_lines+get_bp_branch_inputs()


def get_bp_node_types():
    node_types = _get_file_content(node_types_file_name)
    return node_types


def get_bp_node_templates(bp_name):
    node_templates = _get_file_content(node_templates_file_name)
    return node_templates


def digest_branch(current_node_template_name, current_branch_line, completed_branch_properties,
                  current_branch_lines):

    for excluded_element in excluded_node_template_elements:
        if excluded_element in current_branch_line:
            completed_branch_properties = True
            current_branch_lines.append(current_branch_line)
            return completed_branch_properties, current_branch_lines
    leading_spaces = len(current_branch_line) - len(current_branch_line.lstrip())
    curr_input_raw = current_branch_line.replace("{", "").replace("}", "").lstrip().split(":")
    curr_property_name = curr_input_raw[0].lstrip()

    if len(curr_input_raw) > 2:
        curr_bp_input = curr_input_raw[2].lstrip().strip()
        curr_bp_input_with_colon = "{0}:".format(curr_bp_input)
        if curr_bp_input_with_colon not in bp_inputs_to_be_removed:
            bp_inputs_to_be_removed.append(curr_bp_input_with_colon)
        current_branch_input = "{0}_{1}".format(current_node_template_name, curr_bp_input)
        branches_inputs.append(current_branch_input)
        curr_input_value = "{{ get_input: {0} }}".format(current_branch_input)
    else:
        curr_input_value = curr_input_raw[1].lstrip()

    new_branch_input_line = "{2}{0}: {1}".format(curr_property_name, curr_input_value, leading_spaces*' ')
    current_branch_lines.append(new_branch_input_line)
    return completed_branch_properties, current_branch_lines


def get_current_template_inputs(root_node_template_name, branch_node_template, internal_node_template_names):
    branch_lines = branch_node_template.splitlines()
    current_node_template_name = None
    inside_properties = False
    completed_branch_properties = False
    current_branch_lines = []

    for current_branch_line in branch_lines:
        line_without_leading_spaces = current_branch_line.lstrip()
        if line_without_leading_spaces.startswith("{0}:".format(root_node_template_name)):
            current_node_template_name = root_node_template_name
        else:
            for internal_node_name in internal_node_template_names:
                current_internal_node_name = "{0}_{1}".format(internal_node_name, root_node_template_name)
                if line_without_leading_spaces.startswith("{0}:".format(current_internal_node_name)):
                    current_node_template_name = current_internal_node_name

        if completed_branch_properties:
            current_branch_lines.append(current_branch_line)
            completed_branch_properties = False
            continue

        if line_without_leading_spaces.startswith("#") or ":" not in line_without_leading_spaces:
            current_branch_lines.append(current_branch_line)
            continue

        if "properties:" in current_branch_line:
            inside_properties = True
            current_branch_lines.append(current_branch_line)
            continue

        if inside_properties:
            completed_branch_properties, current_branch_lines = digest_branch(current_node_template_name,
                                                                              current_branch_line,
                                                                              completed_branch_properties,
                                                                              current_branch_lines)
        else:
            current_branch_lines.append(current_branch_line)
    return current_branch_lines


def get_branch_code(branch_node_template_name, branch_name, internal_node_template_names):
    branch_node_template = _get_file_content(branch_file_name)
    branch_node_template = branch_node_template.replace(branch_node_template_name, branch_name)
    for internal_node_template_name in internal_node_template_names:
        branch_node_template = branch_node_template.replace("{0}:".format(internal_node_template_name),
                                                            "{0}_{1}:".format(internal_node_template_name, branch_name))

    current_branch_lines = get_current_template_inputs(branch_name, branch_node_template, internal_node_template_names)
    return current_branch_lines


def get_bp_end(prefix, bp_name, suffix):
    bp_end = _get_file_content(end_bp_file_name)
    return bp_end


def print_all(start_lines, bp_input_lines, node_types_lines, node_templates_lines, branches_lines, end_lines):
    print start_lines
    for curr_line in bp_input_lines:
        print curr_line
    print node_types_lines
    print node_templates_lines
    for curr_line in branches_lines:
        print curr_line
    print end_lines


def create_bp(branch_node_template_name, internal_node_template_names, prefix, bp_name, suffix):
    start_lines = get_bp_start(prefix, bp_name, suffix)
    branches = ["NewYork", "Chicago", "Washington", "Boston"]

    node_types_lines = get_bp_node_types()
    node_templates_lines = get_bp_node_templates(bp_name)

    branches_lines = []
    for curr_branch in branches:
        branches_lines += get_branch_code(branch_node_template_name, curr_branch, internal_node_template_names)

    bp_input_lines = get_bp_inputs()
    end_lines = get_bp_end(prefix, bp_name, suffix)

    print_all(start_lines, bp_input_lines, node_types_lines, node_templates_lines, branches_lines, end_lines)


def main(argv):
    #for i in range(len(argv)):
    #    print ("argv={0}\n".format(argv[i]))

    bp_name = argv[1]
    prefix = "A_"
    suffix = "_bp"
    branch_node_template_name = "branch"
    internal_node_template_names = ["data_center", "conf_room"]
    create_bp(branch_node_template_name, internal_node_template_names, prefix, bp_name, suffix)

if __name__ == '__main__':
    main(sys.argv)

