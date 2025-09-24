import math

class Vector3:
    def __init__(self, x, y, z):
        """Initializes the vector with the supplied elements"""
        self.x = x
        self.y = y
        self.z = z

    @staticmethod
    def zeros():
        return Vector3(0.0, 0.0, 0.0)
    
    def __add__(self, other):
        """Adds two vectors"""
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        """Subtracts one vector from another"""
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar):
        """Scales a vector by a scaler"""
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    def __truediv__(self, scalar):
        """Scales a vector by a scalar through division"""
        return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)
    
    def magnitude2(self):
        """Computes the square of the magnitude vector"""
        return self.x**2 + self.y**2 + self.z**2

    def magnitude(self):
        """Computes the magnitude of the vector"""
        return math.sqrt(self.magnitude2())

    def dot(self, other):
        """Computes the dot product of two vectors"""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        """Computes the cross product of two vectors"""
        cross_x = self.y * other.z - self.z * other.y
        cross_y = self.z * other.x - self.x * other.z
        cross_z = self.x * other.y - self.y * other.x
        return Vector3(cross_x, cross_y, cross_z)
    
    def __str__(self):
        """Returns the vector in string format"""
        return f"[{self.x}, {self.y}, {self.z}]"

class Matrix33:
    def __init__(self, row1: Vector3, row2: Vector3, row3: Vector3):
        """Initializes the matrix using three vectors as respective rows"""
        self.rows = {
            1: row1,
            2: row2,
            3: row3
        }
    
    def at(self, row: int, column: int):
        """Returns the value at a particular row or column. Indexing starts at 1."""
        if row < 1 or row > 3 or column < 1 or column > 3:
            raise ValueError("Index must be 1, 2, or 3")
        if column == 1:
            return self.rows[row].x
        elif column == 2:
            return self.rows[row].y
        elif column == 3:
            return self.rows[row].z
        else:
            assert(False)

    def column(self, index: int):
        """Returns a column of the matrix as a vector"""
        if index < 1 or index > 3:
            raise ValueError("Index must be 1, 2, or 3")
        return Vector3(self.at(1, index), self.at(2, index), self.at(3, index))
    
    def transposed(self):
        """Returns a transposed version of the matrix"""
        return Matrix33(self.column(1), self.column(2), self.column(3))
    
    def __mul__(self, other):
        """Multiplies by matrix by another matrix, a vector, or a scalar"""
        if isinstance(other, (int, float)):
            # Not sure we need this for PSet 2 but including to future-proof
            return Matrix33(self.rows[1] * other, self.rows[2] * other, self.rows[3] * other)
        elif isinstance(other, Vector3):
            return Vector3(self.rows[1].dot(other), self.rows[2].dot(other), self.rows[3].dot(other))
        else:
            raise TypeError("Unsupported operand type(s) for *: 'Matrix33' and '{}'".format(type(other).__name__))