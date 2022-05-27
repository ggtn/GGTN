from collections import OrderedDict
from ..objects.cpg.function import Function
from ..objects.cpg.function_pdg import Function_PDG
from ..objects.cpg.function_cfg import Function_CFG


def order_nodes(nodes, max_nodes):
    # sorts nodes by line and column

    nodes_by_column = sorted(nodes.items(), key=lambda n: n[1].get_column_number())
    nodes_by_line = sorted(nodes_by_column, key=lambda n: n[1].get_line_number())

    for i, node in enumerate(nodes_by_line):
        node[1].order = i

    if len(nodes) > max_nodes:
        print(f"CPG cut - original nodes: {len(nodes)} to max: {max_nodes}")
        return OrderedDict(nodes_by_line[:max_nodes])

    return OrderedDict(nodes_by_line)


def filter_nodes(nodes):
    return {n_id: node for n_id, node in nodes.items() if node.has_code() and
            node.has_line_number() and
            node.label not in ["Comment", "Unknown"]}


def parse_to_nodes_ast(cpg, max_nodes=500):
    ast_nodes = {}
    for function in cpg["functions"]:
        func = Function(function)
        # Only nodes with code and line number are selected
        filtered_ast_nodes = filter_nodes(func.get_ast_nodes())
        ast_nodes.update(filtered_ast_nodes)

    return order_nodes(ast_nodes, max_nodes)

def parse_to_nodes_cfg(cpg, max_nodes=500):
    cfg_nodes = {}
    for function in cpg["functions"]:
        func = Function(function)
        # Only nodes with code and line number are selected
        filtered_cfg_nodes = filter_nodes(func.get_cfg_nodes())
        cfg_nodes.update(filtered_cfg_nodes)


    return order_nodes(cfg_nodes, max_nodes)

def parse_to_nodes_pdg(cpg, max_nodes=500):
    pdg_nodes = {}
    for function in cpg["functions"]:
        func = Function(function)
        # Only nodes with code and line number are selected
        filtered_pdg_nodes = filter_nodes(func.get_pdg_nodes())
        pdg_nodes.update(filtered_pdg_nodes)

    return order_nodes(pdg_nodes, max_nodes)