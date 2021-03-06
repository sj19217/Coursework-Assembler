"""
Holds the code to parse global variables into a dictionary of information.
"""

import logging
from collections import namedtuple
import json

from pycparser.c_ast import Decl, FuncDef

GlobalVariable = namedtuple("GlobalVariable", "name type initial")
GlobalFunction = namedtuple("GlobalFunction", "name definition")

def global_parser(tree, interactive_mode=False) -> dict:
    """
    Takes the syntax tree and generates a dictionary of information.
    """
    table = []

    for top_node in tree:
        if isinstance(top_node, Decl):
            name = top_node.name
            type_list = top_node.type.type.names
            initial = top_node.init

            if "char" in type_list:
                str_type = "char"
            elif "short" in type_list:
                str_type = "short"
            elif "int" in type_list:
                str_type = "int"
            else:
                logging.error("Type is unknown ({0}) for variable {1}".format(type_list, name))
                return

            if "unsigned" in type_list:
                str_type = "u" + str_type

            logging.info("Found global variable {name} of type {type}, initial {init}".format(name=name, type=str_type, init=initial))

            table.append(GlobalVariable(name, str_type, initial))
            if interactive_mode:
                print("found_global", json.dumps([
                    name, str_type, initial.value
                ]))
        elif isinstance(top_node, FuncDef):
            if top_node.decl.name == "main":
                table.append(GlobalFunction("main", top_node))
                logging.info("Found global function main")
            else:
                logging.warning("Found global function that was not main; this is not yet supported")

    return table