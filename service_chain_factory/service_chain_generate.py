import os

import itertools
import sys
import copy
import ServiceChainDictionary


def add_imports(depth, blueprint_name):
    print "{0} In {1}".format(' '*depth, sys._getframe().f_code.co_name)

    print " {0} bp is {1}".format(' '*depth, blueprint_name)

    print "{0} End of {1}".format(' '*depth, sys._getframe().f_code.co_name)


def add_inputs(depth, blueprint_name):
    print "{0} In {1}".format(' '*depth, sys._getframe().f_code.co_name)

    print " {0} bp is {0}".format(' '*depth, blueprint_name)

    print "{0} End of {1}".format(' '*depth, sys._getframe().f_code.co_name)


def add_node_types(depth, blueprint_name):
    print "{0} In {1}".format(' '*depth, sys._getframe().f_code.co_name)

    print " {0} bp is {0}".format(' '*depth, blueprint_name)

    print "{0} End of {1}".format(' '*depth, sys._getframe().f_code.co_name)


def add_node_templates(depth, blueprint_name):
    print "{0} In {1}".format(' '*depth, sys._getframe().f_code.co_name)

    print " {0} bp is {0}".format(' '*depth, blueprint_name)

    print "{0} End of {1}".format(' '*depth, sys._getframe().f_code.co_name)


def add_plugins(depth, blueprint_name):
    print "{0} In {1}".format(' '*depth, sys._getframe().f_code.co_name)

    print " {0} bp is {0}".format(' '*depth, blueprint_name)

    print "{0} End of {1}".format(' '*depth, sys._getframe().f_code.co_name)


def add_workflows(depth, blueprint_name):
    print "{0} In {1}".format(' '*depth, sys._getframe().f_code.co_name)

    print " {0} bp is {0}".format(' '*depth, blueprint_name)

    print "{0} End of {1}".format(' '*depth, sys._getframe().f_code.co_name)


def add_policies(depth, blueprint_name):
    print "{0} In {1}".format(' '*depth, sys._getframe().f_code.co_name)

    print " {0} bp is {0}".format(' '*depth, blueprint_name)

    print "{0} End of {1}".format(' '*depth, sys._getframe().f_code.co_name)

def create_blueprint(blueprint_name):
    print "----------------------------"
    print "In {0}".format(sys._getframe().f_code.co_name)

    print " bp is {0}".format(blueprint_name)
    add_imports(2, blueprint_name)
    add_inputs(2, blueprint_name)
    add_node_types(2, blueprint_name)
    add_node_templates(2, blueprint_name)
    add_plugins(2, blueprint_name)
    add_workflows(2, blueprint_name)
    add_policies(2, blueprint_name)

    print "End of {0}".format(sys._getframe().f_code.co_name)
    print "----------------------------"