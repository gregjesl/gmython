from .resources.prop import Propagator
from .resources.spacecraft import Spacecraft
from .resources.celestial import CelestialBody
from .mission import Propagate, MissionStep, Assignment
from .resources.variable import Variable, Vector

def propagate_to_periapsis(spacecraft: Spacecraft, prop: Propagator, body: CelestialBody) -> Propagate:
    return Propagate(prop, [spacecraft], [(spacecraft.relative_to(body).periapsis(), None)], "Propagate to Periapsis")

def propagate_to_apoapsis(spacecraft: Spacecraft, prop: Propagator, body: CelestialBody) -> Propagate:
    return Propagate(prop, [spacecraft], [(spacecraft.relative_to(body).apoapsis(), None)], "Propagate to Apoapsis")

def angle2(vec1: Vector, vec2: Vector, out: Variable) -> Assignment:
    """Computes the angle between two vectors using the dot product
    
    The behavior is undefined if the norm of either of the vectors is 0
    """
    dot = vec1.dot(vec2)
    norm = f"{vec1.norm2()} * {vec2.norm2()}"
    return Assignment(out, f"acos(({dot})/({norm}))")