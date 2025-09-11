from enum import Enum
from .resource import Resource
from .coordsys import CoordinateSystem
from .celestial import CelestialBody

class LocalCoordinateSystemAxes(Enum):
    VNB = 1,
    LVLH = 2,
    MJ2000Eq = 3,
    SpacecraftBody = 4

class LocalCoordinateSystem:
    def __init__(self, body: CelestialBody, axes: LocalCoordinateSystemAxes):
        self.body = body
        self.axes = axes

class ImpulseiveBurn(Resource):
    def __init__(self, name, coordsys: CoordinateSystem | LocalCoordinateSystem, vector: list = [0.0, 0.0, 0.0]):
        super().__init__(name)
        self.coordsys = coordsys
        if len(vector) != 3:
            raise ValueError("Expecting Delta-V Vector length of 3")
        if not all(isinstance(x, (int, float)) for x in vector):
            raise ValueError("Expecting numbers in Delta-V Vector")
        self.vector = vector
    
    def to_gmat_script(self):
        if isinstance(self.coordsys, LocalCoordinateSystem):
            return (
                f"Create ImpulsiveBurn {self.name};\n"
                f"GMAT {self.name}.CoordinateSystem = Local;\n"
                f"GMAT {self.name}.Origin = {self.coordsys.body.name};\n"
                f"GMAT {self.name}.Axes = {self.coordsys.axes.name};\n"
                f"GMAT {self.name}.Element1 = {self.vector[0]};\n"
                f"GMAT {self.name}.Element2 = {self.vector[1]};\n"
                f"GMAT {self.name}.Element3 = {self.vector[2]};"
            )
        else:
            return (
                    f"Create ImpulsiveBurn {self.name};\n"
                    f"GMAT {self.name}.CoordinateSystem = {self.coordsys.name};\n"
                    f"GMAT {self.name}.Element1 = {self.vector[0]};\n"
                    f"GMAT {self.name}.Element2 = {self.vector[1]};\n"
                    f"GMAT {self.name}.Element3 = {self.vector[2]};\n"
                )

    def element1(self) -> str:
        return f"{self.name}.Element1"
    
    def element2(self) -> str:
        return f"{self.name}.Element2"
    
    def element3(self) -> str:
        return f"{self.name}.Element3"