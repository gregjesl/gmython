from enum import Enum
from .resource import Resource
from .celestial import CelestialBody, EARTH

class CoordinateSystemAxes(Enum):
    MJ2000Eq = 1,
    """An inertial coordinate system. The nominal x-axis points along the line formed by the intersection of the Earth's mean equatorial plane and the mean ecliptic plane (at the J2000 epoch), in the direction of Aries. The z-axis is normal to the Earth's mean equator at the J2000 epoch and the y-axis completes the right-handed system. The mean planes of the ecliptic and equator, at the J2000 epoch, are computed using IAU-1976/FK5 theory with 1980 update for nutation."""
    
    MJ2000Ec = 2,
    """An inertial coordinate system. The x-axis points along the line formed by the intersection of the Earth's mean equator and the mean ecliptic plane at the J2000 epoch. The z-axis is normal to the mean ecliptic plane at the J2000 Epoch and the y-axis completes the right-handed set. This system is computed using IAU-1976/FK5 theory with 1980 update for nutation."""
    
    ICRF = 3,
    """An inertial coordinate system. The axes are close to the mean Earth equator and pole at the J2000 epoch, and at the Earth's surface, the RSS difference between vectors expressed in MJ2000Eq and ICRF is less than 1 m. Note that since MJ2000Eq and ICRF are imperfect realizations of inertial systems, the transformation between them is time varying. This axis system is computed using IAU-2000A theory with 2006 update for precession."""

    LocalAlignedConstrained = 4,
    """The LocalAlignedConstrained axis system is an aligned constrained system based on the position of the ReferenceObject with respect to the Origin and is computed using the well known Triad algorithm. The axes are computed such that the AlignmentVector, defined as the components of the alignment vector expressed in the LocalAlignedConstrained system, is aligned with the position of the ReferenceBody w/r/t the origin. The rotation about the AlignmentVector is resolved by minimizing the angle between the ContraintVector, defined as the constraint vector expressed in the LocalAlignedConstrained system, and the ConstraintReferenceVector, defined as the constraint reference vector expressed in the ConstraintCoordinateSystem. The alignment vectors and the constraint vectors cannot have zero length. Similarly, the cross products of the constraint vector and alignment vector cannot have zero length."""
    
    MODEq = 5,
    """A quasi-inertial coordinate system referenced to Earth's mean equator at the current epoch. The current epoch is defined by the context of use and usually comes from the spacecraft or graphics epoch. This system is computed using IAU-1976/FK5 theory with 1980 update for nutation."""

    MODEc = 6,
    """A quasi-inertial coordinate system referenced to the mean ecliptic at the current epoch. The current epoch is defined by the context of use and usually comes from the spacecraft or graphics epoch. This system is computed using IAU-1976/FK5 theory with 1980 update for nutation."""

    TODEq = 7,
    """A quasi-inertial coordinate system referenced to Earth's true equator at the current epoch. The current epoch is defined by the context of use and usually comes from the spacecraft or graphics epoch. This system is computed using IAU-1976/FK5 theory with 1980 update for nutation."""
    
    TODEc = 8,
    """A quasi-inertial coordinate system referenced to Earth's true ecliptic at the current epoch. The current epoch is defined by the context of use and usually comes from the spacecraft or graphics epoch. This system is computed using IAU-1976/FK5 theory with 1980 update for nutation."""

    MOEEq = 9,
    """A quasi-inertial coordinate system referenced to Earth's mean equator at the reference epoch. The reference epoch is defined on the CoordinateSystem object. This system is computed using IAU-1976/FK5 theory with 1980 update for nutation."""

    MOEEc = 10,
    """A quasi-inertial coordinate system referenced to the mean ecliptic at the reference epoch. The reference epoch is defined on the CoordinateSystem object. This system is computed using IAU-1976/FK5 theory with 1980 update for nutation."""

    TOEEq = 11,
    """A quasi-inertial coordinate system referenced to Earth's true equator at the reference epoch. The reference epoch is defined on the CoordinateSystem object. This system is computed using IAU-1976/FK5 theory with 1980 update for nutation."""

    TOEEc = 12,
    """A quasi-inertial coordinate system referenced to the true ecliptic at the reference epoch. The reference epoch is defined on the CoordinateSystem object. This system is computed using IAU-1976/FK5 theory with 1980 update for nutation."""

    ObjectReferenced = 13,
    """An ObjectReferenced system is a CoordinateSystem whose axes are defined by the motion of one object with respect to another object. See the discussion above for a detailed description of the ObjectReferenced axis system."""

    Equator = 14,
    """A true of date equator axis system for the celestial body selected as the origin. The Equator system is defined by the body's equatorial plane and its intersection with the ecliptic plane, at the current epoch. The current epoch is defined by the context of use and usually comes from the spacecraft or graphics epoch."""

    BodyFixed = 15,
    """The BodyFixed axis system is referenced to the body equator and the prime meridian of the body.
    
    When Origin is a Spacecraft, the axes are computed using the Spacecraft's attitude model. 
    
    Note: not all attitude models compute body rates. In the case that body rates are not available on a spacecraft, a request for velocity transformations using a BodyFixed axis system will result in an error.
    """

    BodyInertial = 16,
    """An inertial system referenced to the equator ( at the J2000 epoch ) of the celestial body selected as the origin of the CoordinateSystem. Because the BodyInertial axis system uses different theories for different bodies, the following definitions describe only the nominal axis configurations. The x-axis points along the line formed by the intersection of the bodies equator and earth's mean equator at J2000. The z-axis points along the body's spin axis direction at the J2000 epoch. The y-axis completes the right-handed set. For Earth, the BodyInertial axis system is identical to the MJ2000Eq system"""

    GSE = 17,
    """The Geocentric Solar Ecliptic system. The x-axis points from Earth to the Sun. The z-axis is defined as the cross product RxV where R and V are earth's position and velocity with respect to the sun respectively. The y-axis completes the right-handed set. The GSE axes are computed using the relative motion of the Earth and Sun even if the origin is not Earth."""

    GSM = 18,
    """The Geocentric Solar Magnetic system. The x-axis points from Earth to the Sun. The z-axis is defined to be orthogonal to the x-axis and lies in the plane of the x-axis and Earth's magnetic dipole vector. The y-axis completes the right-handed set. The GSM axes are computed using the relative motion of the Earth and Sun even if the origin is not Earth."""

    Topocentric = 19,
    """A GroundStation-based coordinate system. The y-axis points due East and the z-axis is normal to the local horizon. The x-axis completes the right handed set."""

    BodySpinSun = 20,
    """A celestial body spin-axis-referenced system. The x-axis points from the celestial body to the Sun. The y-axis is computed as the cross product of the x-axis and the body's spin axis. The z-axis completes the right-handed set."""

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