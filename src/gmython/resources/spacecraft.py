from abc import abstractmethod
import math

from .resource import Resource
from .coordsys import CoordinateSystem, EARTHMJ2000EQ
from .epoch import Epoch, TimeStandard, ModJulianEpoch
from .celestial import CelestialBody

class State:
    @abstractmethod
    def to_gmat_script(self, name: str) -> str:
        pass

class CartesianState(State):
    def __init__(self, x: float, y: float, z: float, vx: float, vy: float, vz: float):
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz

    def to_gmat_script(self, name: str) -> str:
        return (
            f"GMAT {name}.DisplayStateType = Cartesian;\n"
            f"GMAT {name}.X = {self.x};\n"
            f"GMAT {name}.Y = {self.y};\n"
            f"GMAT {name}.Z = {self.z};\n"
            f"GMAT {name}.VX = {self.vx};\n"
            f"GMAT {name}.VY = {self.vy};\n"
            f"GMAT {name}.VZ = {self.vz};"
        )

class KeplerianState(State):
    def __init__(self, sma: float, ecc: float, inc: float, raan: float, aop: float, ta: float):
        self.sma = sma    # Semi-major axis
        self.ecc = ecc    # Eccentricity
        self.inc = inc    # Inclination
        self.raan = raan  # Right Ascension of Ascending Node
        self.aop = aop    # Argument of Periapsis
        self.ta = ta      # True Anomaly

    def to_gmat_script(self, name: str) -> str:
        return (
            f"GMAT {name}.DisplayStateType = Keplerian;\n"
            f"GMAT {name}.SMA = {self.sma};\n"
            f"GMAT {name}.ECC = {self.ecc};\n"
            f"GMAT {name}.INC = {self.inc};\n"
            f"GMAT {name}.RAAN = {self.raan};\n"
            f"GMAT {name}.AOP = {self.aop};\n"
            f"GMAT {name}.TA = {self.ta};"
        )
      
    @staticmethod
    def periapsis(sma: float, ecc: float, inc: float, raan: float, aop: float):
        """Creates a Keplerian orbit starting at periapsis"""
        return KeplerianState(sma, ecc, inc, raan, aop, 0.0)
    
    @staticmethod
    def apoapsis(sma: float, ecc: float, inc: float, raan: float, aop: float):
        """Creates a Keplerian orbit starting at apoapsis"""
        return KeplerianState(sma, ecc, inc, raan, aop, 180.0)
    
    def eccentric_anomaly(self) -> float:
        """Converts the true anomaly to eccentric anomaly"""
        scale = math.sqrt((1.0 + self.ecc) / (1.0 - self.ecc))
        lhs = math.tan(math.radians(self.ta) / 2.0) / scale
        return math.degrees(math.atan(lhs)) * 2.0
    
    def r_mag(self) -> float:
        """Computes the magnitude of the position vector"""
        return self.sma * (1.0 - (self.ecc * math.cos(math.radians(self.eccentric_anomaly()))))

class ModifiedKeplerianState(State):
    def __init__(self, radper: float, radapo: float, inc: float, raan: float, aop: float, ta: float):
        if radapo < radper:
            raise Exception("Apoapsis radius must be larger than periapsis radius")
        self.radper = radper    # Radius of perigee
        self.radapo = radapo    # Radius of apogee
        self.inc = inc    # Inclination
        self.raan = raan  # Right Ascension of Ascending Node
        self.aop = aop    # Argument of Periapsis
        self.ta = ta      # True Anomaly

    def to_gmat_script(self, name: str) -> str:
        return (
            f"GMAT {name}.DisplayStateType = Keplerian;\n"
            f"GMAT {name}.RadApo = {self.radapo};\n"
            f"GMAT {name}.RadPer = {self.radper};\n"
            f"GMAT {name}.INC = {self.inc};\n"
            f"GMAT {name}.RAAN = {self.raan};\n"
            f"GMAT {name}.AOP = {self.aop};\n"
            f"GMAT {name}.TA = {self.ta};"
        )

class BodyRelativeProperties:
    def __init__(self, name: str, body: CelestialBody):
        self.preamble = f"{name}.{body.name}."

    def periapsis(self) -> str:
        return self.preamble + "Periapsis"
    
    def apoapsis(self) -> str:
        return self.preamble + "Apoapsis"
    
    def rmag(self) -> str:
        return self.preamble + "RMAG"
    
    def sma(self) -> str:
        return self.preamble + "SMA"
    
    def ecc(self) -> str:
        return self.preamble + "ECC"
    
    def apoapsis_radius(self) -> str:
        return self.preamble + "RadApo"
    
    def periapsis_radius(self) -> str:
        return self.preamble + "RadPer"
    
    def orbit_period(self) -> str:
        return self.preamble + "OrbitPeriod"
    
    def beta_angle(self) -> str:
        return self.preamble + "BetaAngle"
    
    def C3Energy(self) -> str:
        return self.preamble + "C3Energy"
    
    def energy(self) -> str:
        return self.preamble + "Energy"
    
    def h_mag(self) -> str:
        """Magnitude of the angular velocity vector"""
        return self.preamble + "HMAG"

    def incoming_C3_energy(self) -> str:
        return self.preamble + "IncomingC3Energy"
    
    def incoming_rad_per(self) -> str:
        return self.preamble + "IncomingRadPer"
    
    def latitude(self) -> str:
        """Planetodetic latitude"""
        return self.preamble + "Latitude (degrees)"
    
    def longitude(self) -> str:
        """Planetodetic longitude"""
        return self.preamble + "Longitude (degrees)"
    
    def local_sidereal_time(self) -> str:
        """Local sidereal time of the spacecraft from the celestial body's inertial x-axis (degrees)"""
        return self.preamble + "LST"
    
    def apoapsis_velocity(self):
        """Scalar velocity at apoapsis (km/s)"""
        return self.preamble + "VelApoapsis"
    
    def periapsis_velocity(self):
        """Scalar velocity at periapsis (km/s)"""
        return self.preamble + "VelPeriapsis"

class Spacecraft(Resource):
    def __init__(self, name: str, state: State, epoch: Epoch = ModJulianEpoch(TimeStandard.TAI, 21545.0), coord_system: CoordinateSystem = EARTHMJ2000EQ) -> None:
        super().__init__(name)
        self.name = name
        self.state = state
        self.epoch = epoch
        self.coordinate_system = coord_system

    def to_gmat_script(self) -> str:
        base_script = (
            f"Create Spacecraft {self.name};\n"
            f"{self.epoch.to_gmat(self.name)}"
            f"GMAT {self.name}.CoordinateSystem = {self.coordinate_system.name};\n"
        )
        state_script = self.state.to_gmat_script(self.name)
        return base_script + state_script
    
    def relative_to(self, body: CelestialBody) -> BodyRelativeProperties:
        return BodyRelativeProperties(self.name, body)
    
    def elapsed_days(self) -> str:
        return f"{self.name}.ElapsedDays"
    
    def elapsed_secs(self) -> str:
        return f"{self.name}.ElapsedSecs"