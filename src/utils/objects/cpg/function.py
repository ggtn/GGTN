from .ast import AST
from .cfg import CFG
from .pdg import PDG

class Function:
    def __init__(self, function):
        self.name = function["function"]
        self.id = function["id"].split(".")[-1]
        self.indentation = 1
        self.ast = AST(function["AST"], self.indentation)
        self.cfg = CFG(function["CFG"], self.indentation)
        self.pdg = PDG(function["PDG"], self.indentation)

    def __str__(self):
        indentation = self.indentation * "\t"
        return f"{indentation}Function Name: {self.name}\n{indentation}Id: {self.id}\n{indentation}AST:{self.ast}\n{indentation}CFG:{self.cfg}\n{indentation}PDG:{self.pdg}"

    def get_ast_nodes(self):
        return self.ast.nodes
    def get_cfg_nodes(self):
        return self.cfg.nodes
    def get_pdg_nodes(self):
        return self.pdg.nodes

    def get_nodes_types(self):
        return self.ast.get_nodes_type()
