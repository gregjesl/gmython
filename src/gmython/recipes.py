from .resources.prop import Propagator
from .resources.spacecraft import Spacecraft
from .resources.celestial import CelestialBody
from .mission import Propagate, MissionStep, Assignment, IfBlock, Condition, Comparison
from .resources.variable import Variable, Vector
from .resources.coordsys import CoordinateSystem

def propagate_to_periapsis(spacecraft: Spacecraft, prop: Propagator, body: CelestialBody) -> Propagate:
    return Propagate(prop, [spacecraft], [(spacecraft.relative_to(body).periapsis(), None)], description="Propagate to Periapsis")

def propagate_to_apoapsis(spacecraft: Spacecraft, prop: Propagator, body: CelestialBody) -> Propagate:
    return Propagate(prop, [spacecraft], [(spacecraft.relative_to(body).apoapsis(), None)], description="Propagate to Apoapsis")

def propagate_to_ascending_node(spacecraft: Spacecraft, prop: Propagator, frame: CoordinateSystem) -> list[MissionStep]:
    step = Propagate(prop, [spacecraft], [(str(spacecraft.with_frame(frame).z), 0.0)])
    ascend = IfBlock(Condition(spacecraft.with_frame(frame).vz, Comparison.LESS_THAN, 0.0))
    ascend.append(step)
    return [step, ascend]

def propagate_to_descending_node(spacecraft: Spacecraft, prop: Propagator, frame: CoordinateSystem) -> list[MissionStep]:
    step = Propagate(prop, [spacecraft], [(str(spacecraft.with_frame(frame).z), 0.0)])
    ascend = IfBlock(Condition(spacecraft.with_frame(frame).vz, Comparison.GREATER_THAN, 0.0))
    ascend.append(step)
    return [step, ascend]

def angle2(vec1: Vector, vec2: Vector, out: Variable) -> Assignment:
    """Computes the angle between two vectors using the dot product
    
    The behavior is undefined if the norm of either of the vectors is 0
    """
    dot = vec1.dot(vec2)
    norm = f"{vec1.norm2()} * {vec2.norm2()}"
    return Assignment(out, f"acos(({dot})/({norm}))")