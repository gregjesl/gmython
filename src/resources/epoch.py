from abc import ABC, abstractmethod
from enum import Enum

class TimeStandard(Enum):
    TAI = 1
    """International Atomic Time"""

    UTC = 2
    """Coordinated Universal Time"""

    TDB = 3
    """Barycentric Dynamical Time"""

    TT = 4
    """Terrestrial Time"""

class Epoch(ABC):
    def __init__(self, standard: TimeStandard):
        self.standard = standard
        super().__init__()

    @abstractmethod
    def to_gmat(self, name: str) -> str:
        pass

class ModJulianEpoch(Epoch):
    def __init__(self, standard: TimeStandard, time: float):
        super().__init__(standard)
        self.time = time

    def to_gmat(self, name: str) -> str:
        return f"GMAT {name}.DateFormat = {self.standard.name}ModJulian;\nGMAT {name}.Epoch = {self.time};\n"
    
from datetime import datetime

class GregorianEpoch(Epoch):
    def __init__(self, standard: TimeStandard, day: int, month: int, year: int,
                 hour: int = 0, minute: int = 0, second: int = 0, millisecond: int = 0):
        super().__init__(standard)

        # Validate ranges
        if not (1 <= month <= 12):
            raise ValueError(f"Month must be between 1 and 12, got {month}")
        if not (1 <= day <= 31):
            raise ValueError(f"Day must be between 1 and 31, got {day}")
        if not (0 <= hour <= 23):
            raise ValueError(f"Hour must be between 0 and 23, got {hour}")
        if not (0 <= minute <= 59):
            raise ValueError(f"Minute must be between 0 and 59, got {minute}")
        if not (0 <= second <= 59):
            raise ValueError(f"Second must be between 0 and 59, got {second}")
        if not (0 <= millisecond <= 999):
            raise ValueError(f"Millisecond must be between 0 and 999, got {millisecond}")

        # Validate actual date (e.g., no Feb 30)
        try:
            _ = datetime(year, month, day, hour, minute, second, millisecond * 1000)
        except ValueError as e:
            raise ValueError(f"Invalid date: {e}")

        self.day = day
        self.month = month
        self.year = year
        self.hour = hour
        self.minute = minute
        self.second = second
        self.millisecond = millisecond

    def to_string(self) -> str:
        microsecond = self.millisecond * 1000
        dt = datetime(self.year, self.month, self.day, self.hour, self.minute, self.second, microsecond)
        return dt.strftime("%d %b %Y %H:%M:%S.") + f"{int(dt.microsecond / 1000):03d}"

    def to_gmat(self, name: str) -> str:
        return f"GMAT {name}.DateFormat = {self.standard.name}Gregorian;\nGMAT {name}.Epoch = '{self.to_string()}';\n"
