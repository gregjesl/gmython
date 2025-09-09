from enum import Enum
from .resource import Resource

class DCAlgorithm(Enum):
    NewtonRaphson = 1
    Broyden = 2
    ModifiedBroyden = 3

class DCDerivativeMethod(Enum):
    CentralDifference = 1
    ForwardDifference = 2
    BackwardDifference = 3

class DifferentialCorrector(Resource):
    def __init__(self, name, algorithm: DCAlgorithm = DCAlgorithm.NewtonRaphson, max_iter: int = 25, derivative_method = DCDerivativeMethod.ForwardDifference):
        super().__init__(name)
        self.algorithm = algorithm
        self.max_iter = max_iter
        self.derivative_method = derivative_method
    
    def to_gmat_script(self):
        return (
                f"Create DifferentialCorrector {self.name};\n"
                f"GMAT {self.name}.ShowProgress       = false;\n"
                f"GMAT {self.name}.MaximumIterations  = {self.max_iter};\n"
                f"GMAT {self.name}.DerivativeMethod   = {self.derivative_method.name};\n"
                f"GMAT {self.name}.Algorithm          = {self.algorithm.name};"
            )