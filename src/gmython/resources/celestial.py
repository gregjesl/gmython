class CelestialBody:
    def __init__(self, name: str, radius: float):
        self.name = name
        self.radius = radius
    
    def radius_of_altitude(self, altitude: float) -> float:
        return self.radius + altitude
    
    def altitude_of_radius(self, radius: float) -> float:
        return radius - self.radius

# Constants for each celestial body
SUN = CelestialBody("Sun", 696340)
MERCURY = CelestialBody("Mercury", 2439.7)
VENUS = CelestialBody("Venus", 6051.8)
EARTH = CelestialBody("Earth", 6371.0)
MARS = CelestialBody("Mars", 3389.5)
JUPITER = CelestialBody("Jupiter", 69911)
SATURN = CelestialBody("Saturn", 58232)
URANUS = CelestialBody("Uranus", 25362)
NEPTUNE = CelestialBody("Neptune", 24622)
PLUTO = CelestialBody("Pluto", 1188.3)
LUNA = CelestialBody("Luna", 1737.5)  # Luna is another name for Earth's Moon
