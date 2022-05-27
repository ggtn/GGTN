from .pdg import PDG


class Function_PDG:
    def __init__(self, function):
        self.name = function["function"]
        self.id = function["id"].split(".")[-1]
        self.indentation = 1
        self.pdg = PDG(function["PDG"], self.indentation)

    def __str__(self):
        indentation = self.indentation * "\t"
        return f"{indentation}Function Name: {self.name}\n{indentation}Id: {self.id}\n{indentation}PDG:{self.ast}"

    def get_nodes(self):
        return self.pdg.nodes

    def get_nodes_types(self):
        return self.pdg.get_nodes_type()
