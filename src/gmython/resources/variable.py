from .resource import Resource

class Variable(Resource):
    def __init__(self, name: str):
        super().__init__(name)

    def __str__(self) -> str:
        return self.name
    
    def power(self, x) -> str:
        return f"{self.name}^{x}"

    def to_gmat_script(self):
        return "Create Variable " + self.name + ";"
    
class ArrayValue:
    def __init__(self, array: str, row: int, column: int) -> None:
        self.array = array
        self.row = row
        self.column = column

    def __str__(self) -> str:
        return f"{self.array}({self.row},{self.column})"
    
class Array(Resource):
    def __init__(self, name: str, rows: int, columns: int) -> None:
        if rows < 1:
            raise ValueError("Rows must be at least 1")
        if columns < 1:
            raise ValueError("Columns must be at least 1")
        super().__init__(name)
        self.rows = rows
        self.columns = columns
    
    def at(self, row: int, column: int) -> ArrayValue:
        """WARNING: Indicies start at 1 in GMAT"""
        if row < 1:
            raise ValueError("Row must be at least 1")
        if column < 1:
            raise ValueError("Column must be at least 1")
        if row > self.rows:
            raise ValueError("Row index out of bounds")
        if column > self.columns:
            raise ValueError("Column index out of bound")
        return ArrayValue(self.name, row, column)
    
    def transpose(self) -> str:
        return f"{self.name}'"
    
    def dot(self, other) -> str:
        return f"{self.transpose()} * {other.name}"
    
    def cross(self, other) -> str:
        return f"cross({self.name},{other.name})"
    
    def norm2(self) -> str:
        return f"norm({self.name})"
    
    def det(self) -> str:
        return f"det({self.name})"
    
    def inv(self) -> str:
        return f"inv({self.name})"
    
    @staticmethod
    def randn(n: int) -> str:
        """nxn matrix containing pseudorandom values drawn from the standard normal distribution
        
        The array must already exist
        """
        return f"randn({n})"
    
    def to_gmat_script(self):
        return f"Create Array {self.name}[{self.rows},{self.columns}];"
    
class Vector(Array):
    """GMAT does not explicitly define vectors, this is a helper class that creates a nx1 array"""
    def __init__(self, name: str, rows: int) -> None:
        super().__init__(name, rows, 1)

    def __getitem__(self, index) -> ArrayValue:
        if index < 1:
            raise ValueError("GMAT indexing starts at 1")
        return ArrayValue(self.name, index, 1)
   
    def to_gmat_script(self):
        return f"Create Array {self.name}[{self.rows},1];"
    
    @staticmethod
    def vector2(name: str):
        return Vector(name, 2)
    
    @staticmethod
    def vector3(name: str):
        return Vector(name, 3)