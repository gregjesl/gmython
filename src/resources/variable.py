from .resource import Resource

class Variable(Resource):
    def __init__(self, name: str):
        super().__init__(name)

    def to_gmat_script(self):
        return "Create Variable " + self.name + ";"