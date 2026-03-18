from typing import Any
    
def sin(angle: Any) -> str:
    """Sine (radians)"""
    return f"sin({angle})"

def cos(angle: Any) -> str:
    """Cosine (radians)"""
    return f"cos({angle})"

def tan(angle: Any) -> str:
    """Tangent (radians)"""
    return f"tan({angle})"

def asin(x: Any) -> str:
    """Arcsine (radians)"""
    return f"asin({x})"

def acos(x: Any) -> str:
    """Arccosine (radians)"""
    return f"acos({x})"

def atan(x: Any) -> str:
    """Arctangent (radians)"""
    return f"atan({x})"

def atan2(y: Any, x: Any) -> str:
    """Arctan(y/x) (radians)"""
    return f"atan({y}, {x})"

def log(x: Any) -> str:
    return f"log({x})"

def log10(x: Any) -> str:
    return f"log10({x})"

def DegToRad(angle: Any) -> str:
    """Degrees to Radians"""
    return f"DegToRad({angle})"

def RadToDeg(angle: Any) -> str:
    """Radians to Degrees"""
    return f"RadToDeg({angle})"

def abs(x: Any) -> str:
    """Absolute value"""
    return f"abs({x})"

def sqrt(x: Any) -> str:
    """Square root"""
    return f"sqrt({x})"