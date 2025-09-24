from .algebra import Vector3

def accel(mu: float, point_r: Vector3, mass_r: Vector3 = Vector3(0.0, 0.0, 0.0)) -> Vector3:
    # Compute the relative vector
    rel_r = point_r - mass_r

    # Compute the magnitude
    mag2 = rel_r.magnitude2()

    if mag2 == 0.0:
        return Vector3.zeros()
    
    return (rel_r * -mu) / mag2