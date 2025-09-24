import math
from .numerical import root_find

class Anomaly:
    def __init__(self, value: float, e: float):
        """Initializes the instance with an angle and an ecentricity"""
        if e < 0.0 or e >= 1.0:
            raise ValueError(f"Eccentricity is not elliptical ({e} supplied)")
        self.value = value
        self.e = e
    
    def cos(self):
        """Returns the cosine of the angle"""
        return math.cos(self.value)
    
    def sin(self):
        """Returns the sine of the angle"""
        return math.sin(self.value)
    
    def tan(self):
        """Returns the tangent of the angle"""
        return math.tan(self.value)

class TrueAnomaly(Anomaly):
    def to_eccentric_anomaly(self):
        """Converts from true anomaly to eccentric anomaly"""
        scale = math.sqrt((1.0 + self.e) / (1.0 - self.e))
        lhs = math.tan(self.value / 2.0) / scale
        result = math.atan(lhs) * 2.0
        return EccentricAnomaly(result, self.e)
    
    def __add__(self, other):
        """Adds an angle"""
        if self.e != other.e:
            raise ValueError("Eccentricity mismatch")
        return TrueAnomaly(self.value + other.value, self.e)

    def __sub__(self, other):
        """Subtracts an angle"""
        if self.e != other.e:
            raise ValueError("Eccentricity mismatch")
        return TrueAnomaly(self.value - other.value, self.e)
    
    @staticmethod
    def periapsis(e: float):
        """Returns an instance that represents periapsis"""
        return TrueAnomaly(0.0, e)
    
    @staticmethod
    def apoapsis(e: float):
        """Returns an instance that represents apoapsis"""
        return TrueAnomaly(math.pi, e)

class EccentricAnomaly(Anomaly):
    def to_mean_anomaly(self):
        """Converts from eccentric anomaly to mean anomaly"""
        result = self.value - (self.e * math.sin(self.value))
        return MeanAnomaly(result, self.e)
    
    def to_true_anomaly(self):
        """Converts from eccentric anomaly to true anomaly"""
        scale = math.sqrt((1.0 + self.e) / (1.0 - self.e))
        rhs = scale * math.tan(self.value / 2.0)
        result = math.atan(rhs) * 2.0
        return TrueAnomaly(result, self.e)
    
    def __add__(self, other):
        """Adds an angle"""
        if self.e != other.e:
            raise ValueError("Eccentricity mismatch")
        return EccentricAnomaly(self.value + other.value, self.e)

    def __sub__(self, other):
        """Subtracts an angle"""
        if self.e != other.e:
            raise ValueError("Eccentricity mismatch")
        return EccentricAnomaly(self.value - other.value, self.e)
    
    @staticmethod
    def periapsis(e: float):
        """Returns an instance that represents periapsis"""
        return EccentricAnomaly(0.0, e)
    
    @staticmethod
    def apoapsis(e: float):
        """Returns an instance that represents apoapsis"""
        return EccentricAnomaly(math.pi, e)

class MeanAnomaly(Anomaly):
    def to_eccentric_anomaly(self):
        def f(x):
            return self.value - (x - (self.e * math.sin(x)))

        def fprime(x):
            return - (1.0 - (self.e * math.cos(x)))
        
        result = root_find(f, fprime, self.value, 1e-9)
        return EccentricAnomaly(result, self.e)
    
    def __add__(self, other):
        """Adds an angle"""
        if self.e != other.e:
            raise ValueError("Eccentricity mismatch")
        return MeanAnomaly(self.value + other.value, self.e)

    def __sub__(self, other):
        """Subtracts an angle"""
        if self.e != other.e:
            raise ValueError("Eccentricity mismatch")
        return MeanAnomaly(self.value - other.value, self.e)
    
    @staticmethod
    def periapsis(e: float):
        """Returns an instance that represents periapsis"""
        return MeanAnomaly(0.0, e)
    
    @staticmethod
    def apoapsis(e: float):
        """Returns an instance that represents apoapsis"""
        return MeanAnomaly(math.pi, e)
    
    def propagate(self, mean_motion: float, time: float):
        """Computes a future mean anomaly given mean motion and time"""
        return MeanAnomaly(self.value + (mean_motion * time), self.e)

import unittest
class AnomalyUnitTest(unittest.TestCase):
    def test_true_to_eccentric(self):
        test = TrueAnomaly(1.0, 0.1)
        self.assertAlmostEqual(test.value, test.to_eccentric_anomaly().to_true_anomaly().value)

    def test_eccentric_to_mean(self):
        test = EccentricAnomaly(1.0, 0.1)
        self.assertAlmostEqual(test.value, test.to_mean_anomaly().to_eccentric_anomaly().value)

    def test_circular(self):
        test = TrueAnomaly(math.pi / 2.0, 0.0)
        self.assertAlmostEqual(test.to_eccentric_anomaly().value, math.pi / 2.0)
        self.assertAlmostEqual(test.to_eccentric_anomaly().to_mean_anomaly().value, math.pi / 2.0)
        test = MeanAnomaly(math.pi / 2.0, 0.0)
        self.assertAlmostEqual(test.to_eccentric_anomaly().value, math.pi / 2.0)
        self.assertAlmostEqual(test.to_eccentric_anomaly().to_true_anomaly().value, math.pi / 2.0)

if __name__ == '__main__':
    unittest.main()