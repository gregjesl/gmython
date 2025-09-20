from enum import Enum
from .resource import Resource
from .celestial import CelestialBody, EARTH

class CoordinateSystemAxes(Enum):
    MJ2000Eq = 1,
    MJ2000Ec = 2,
    BodyFixed = 3,
    BodyInertial = 4

PREDEFINED_COORDINATE_SYSTEMS = ["EarthMJ2000Eq", "EarthMJ2000Ec", "EarthFixed", "EarthICRF"]

class CoordinateSystem(Resource):
    def __init__(self, name, origin: CelestialBody, axes: CoordinateSystemAxes | None) -> None:
        super().__init__(name)
        self.origin = origin.name
        if self.name not in PREDEFINED_COORDINATE_SYSTEMS and axes is None:
            raise ValueError("Axes not defined")
        self.axes = axes

    def to_gmat_script(self) -> str:
        if self.name in PREDEFINED_COORDINATE_SYSTEMS:
            return ""
        elif self.axes is not None:
            return (
                f"Create CoordinateSystem {self.name};\n"
                f"GMAT {self.name}.Origin = {self.origin};\n"
                f"GMAT {self.name}.Axes = {self.axes.name};"
            )
        else:
            raise ValueError("Axes must be defined for non-predefined coordinate systems")

EARTHMJ2000EQ = CoordinateSystem("EarthMJ2000Eq", EARTH, None)

EARTHMJ2000EC = CoordinateSystem("EarthMJ2000Ec", EARTH, None)

EARTHFIXED = CoordinateSystem("EarthFixed", EARTH, None)

EARTHICRF = CoordinateSystem("EarthICRF", EARTH, None)
"""International Celestial Reference Frame"""