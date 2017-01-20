import sys

start_bp_file_name = "bp_start.yaml"
inputs_section_file_name = "inputs_section.yaml"
node_types_file_name = "node_types.yaml"
node_templates_file_name = "node_templates.yaml"
branch_file_name = "branch.yaml"
end_bp_file_name = "bp_end.yaml"

bp_inputs = ["input1", "input2"]


def _get_file_content(file_name):
    with open(file_name, 'r') as f:
        file_content = f.read()
    f.close()
    return file_content


def get_bp_start(prefix, bp_name, suffix):
    #print "{0}: {1}{2}{3}".format("get_bp_start", prefix, bp_name, suffix)
    #print "{0}".format(start_bp_file_name)
    bp_start = _get_file_content(start_bp_file_name)
    print bp_start


def get_bp_branch_inputs(branch_name, branch_inputs):
    for curr_input in branch_inputs:
        print "  {0}_{1}_{2}: ".format(branch_name, "input", curr_input)
        print "    default: \"\""


def get_other_inputs():
    inputs_section = _get_file_content(inputs_section_file_name)
    print inputs_section
    #print "{0}".format("inputs:")
    #for curr_input in bp_inputs:
    #    print "inputs {0}".format(curr_input)


def get_bp_inputs(branches, branch_inputs):
    get_other_inputs()
    for branch_name in branches:
        get_bp_branch_inputs(branch_name, branch_inputs)


def get_bp_node_types(bp_name):
    node_types = _get_file_content(node_types_file_name)
    print node_types

def get_bp_node_templates(bp_name):
    node_templates = _get_file_content(node_templates_file_name)
    print node_templates


def get_branch_inputs(branch_name, branch_inputs):
    print "    properties"
    for curr_input in branch_inputs:
        print "      {{ {0}: {1}_{2}_{3} }}".format("get_input", branch_name, "input", curr_input)
    print " "


def get_branch_code(branch_node_template_name, branch_name, branches_inputs):
    branc_node_template = _get_file_content(branch_file_name)
    branc_node_template = branc_node_template.replace(branch_node_template_name, branch_name)
    print "{0}".format(branc_node_template)
    get_branch_inputs(branch_name, branches_inputs)


def get_bp_end(prefix, bp_name, suffix):
    #print "{0}: {1}{2}{3}".format("get_bp_end", prefix, bp_name, suffix)
    #print "{0}".format(end_bp_file_name)
    bp_end = _get_file_content(end_bp_file_name)
    print bp_end


def create_bp(branch_node_template_name, prefix, bp_name, suffix):
    get_bp_start(prefix, bp_name, suffix)
    branches = ["TelAviv", "Jerusalem"]
    branch_inputs = ["Serial", "LTE", "VDSL"]
    get_bp_inputs(branches, branch_inputs)

    get_bp_node_types(bp_name)
    get_bp_node_templates(bp_name)

    for curr_branch in branches:
        get_branch_code(branch_node_template_name, curr_branch, branch_inputs)
    get_bp_end(prefix, bp_name, suffix)


def main(argv):
    #for i in range(len(argv)):
    #    print ("argv={0}\n".format(argv[i]))

    bp_name = argv[1]
    prefix = "A_"
    suffix = "_bp"
    branch_node_template_name = "branch"
    create_bp(branch_node_template_name, prefix, bp_name, suffix)

if __name__ == '__main__':
    main(sys.argv)
