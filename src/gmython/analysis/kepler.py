from .algebra import Vector3, Matrix33
import math

class KeplerianOrbit:
    def __init__(self, mu: float, h: Vector3, ecc: Vector3, a: float):
        self.mu = mu
        self.h = h
        self.ecc = ecc
        self.a = a

    @staticmethod
    def from_position_velocity(mu: float, r0: Vector3, rdot0: Vector3):
        """Returns the orbit and eccentric anomaly given a position and velocity"""

        # Compute the specific angular momentum vector
        h = r0.cross(rdot0)

        # Compute the eccentricity vector
        ecc = (rdot0.cross(h) / mu) - (r0 / r0.magnitude())

        # Compute the specific energy of the orbit using the vis viva equation
        se = ((rdot0.magnitude() ** 2) / 2.0) - (mu / r0.magnitude())

        # Compute the semi-major axis using the specific energy
        a = -mu / (2.0 * se)

        # Return the result
        orbit = KeplerianOrbit(mu, h, ecc, a)

        # Compute the eccentric anomaly
        sigma = r0.dot(rdot0) / math.sqrt(mu)
        ecc_anom = math.atan2(sigma / math.sqrt(a), 1.0 - (r0.magnitude() / a))

        return orbit, ecc_anom
    
    @staticmethod 
    def from_elements(mu: float, a: float, e: float, i: float, raan: float, aop: float):
        """Returns the orbit given orbital parameters"""
        A11 = (math.cos(raan) * math.cos(aop)) - (math.sin(raan) * math.sin(aop) * math.cos(i))
        A12 = (math.sin(raan) * math.cos(aop)) + (math.cos(raan) * math.sin(aop) * math.cos(i))
        A13 = math.sin(aop) * math.sin(i)
        A31 = math.sin(raan) * math.sin(i)
        A32 = -math.cos(raan) * math.sin(i)
        A33 = math.cos(i)

        ecc = Vector3(A11, A12, A13) * e # Eccentricity vector
        rp = a * (1.0 - e) # Radius of perigee
        vp = math.sqrt((mu / a) * (1.0 + e) / (1.0 - e)) # Velocity of perigee
        h_mag = rp * vp # Magnitude of angular momentum
        h = Vector3(A31, A32, A33) * h_mag # Angular momentum
        return KeplerianOrbit(mu, h, ecc, a)

    def r_mag(self, ecc_anom: float):
        """Returns the magnitude of the position vector at the given eccentric anomaly"""
        return self.a * (1.0 - (self.e() * math.cos(ecc_anom)))
    
    def in_plane_position(self, ecc_anom: float) -> Vector3:
        """Returns the position vector in the orbital plane"""
        return Vector3( \
            self.a * (math.cos(ecc_anom) - self.e()), \
            self.a * math.sqrt(1 - (self.e() ** 2)) * math.sin(ecc_anom), \
            0.0)
    
    def in_plane_velocity(self, ecc_anom: float) -> Vector3:
        """Returns the velocity vector in the orbital plane"""
        return Vector3( \
            -math.sqrt(self.mu * self.a) * math.sin(ecc_anom) / self.r_mag(ecc_anom), \
            math.sqrt(self.mu * self.a * (1.0 - (self.e() ** 2))) * math.cos(ecc_anom) / self.r_mag(ecc_anom), \
            0.0)
    
    def to_position_velocity(self, ecc_anom: float):
        dcm: Matrix33 = self.dcm().transposed()
        pos = dcm * self.in_plane_position(ecc_anom)
        vel = dcm * self.in_plane_velocity(ecc_anom)
        return pos, vel

    def sma(self):
        return self.a
    
    def semi_latus_rectum(self):
        return self.a * (1.0 - (self.ecc.magnitude() ** 2))

    def e(self):
        return self.ecc.magnitude()
    
    def dcm(self):
        ie = self.ecc / self.ecc.magnitude()
        ih = self.h / self.h.magnitude()
        return Matrix33(ie, ih.cross(ie), ih)
    
    def inc(self):
        return math.acos(self.dcm().at(3,3))
    
    def raan(self):
        dcm = self.dcm()
        result = math.atan2(dcm.at(3,1), -dcm.at(3,2))
        if result < 0:
            result += 2.0 * math.pi
        return result
    
    def arg_periapsis(self):
        dcm = self.dcm()
        result = math.atan2(dcm.at(1,3), dcm.at(2,3))
        if result < 0:
            result += 2.0 * math.pi
        return result
    
    def mean_motion(self):
        return math.sqrt(self.mu / (self.a ** 3))
    
    def period(self):
        return 2.0 * math.pi / self.mean_motion()
    