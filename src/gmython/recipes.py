from .resources.prop import Propagator
from .resources.spacecraft import Spacecraft
from .resources.celestial import CelestialBody
from .mission import Propagate, MissionStep

def propagate_to_periapsis(spacecraft: Spacecraft, prop: Propagator, body: CelestialBody) -> Propagate:
    return Propagate(prop, [spacecraft], [(spacecraft.relative_to(body).periapsis(), None)], "Propagate to Periapsis")

def propagate_to_apoapsis(spacecraft: Spacecraft, prop: Propagator, body: CelestialBody) -> Propagate:
    return Propagate(prop, [spacecraft], [(spacecraft.relative_to(body).apoapsis(), None)], "Propagate to Apoapsis")