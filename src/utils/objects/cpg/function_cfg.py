from .cfg import CFG


class Function_CFG:
    def __init__(self, function):
        self.name = function["function"]
        self.id = function["id"].split(".")[-1]
        self.indentation = 1
        self.cfg = CFG(function["CFG"], self.indentation)

    def __str__(self):
        indentation = self.indentation * "\t"
        return f"{indentation}Function Name: {self.name}\n{indentation}Id: {self.id}\n{indentation}AST:{self.ast}"

    def get_nodes(self):
        return self.cfg.nodes

    def get_nodes_types(self):
        return self.cfg.get_nodes_type()
