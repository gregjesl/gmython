from abc import ABC, abstractmethod
from enum import Enum
from contextlib import contextmanager
from .resources.resource import Resource
from .mission import MissionStep
from .resources.spacecraft import State, Epoch, TimeStandard, ModJulianEpoch, CoordinateSystem, EARTHMJ2000EQ, Spacecraft

class ObjectType(Enum):
    RESOURCE = 1
    MISSION_STEP = 2

class ScriptObject(ABC):
    def __init__(self, name: str, type: ObjectType) -> None:
        self.name = name
        self.type = type

    @abstractmethod
    def to_gmat_script(self) -> str:
        pass

class Script:
    def __init__(self, resources: list[Resource] | None = None, mission: list[MissionStep] | None = None) -> None:
        self.resources = resources if resources is not None else []
        self.mission = mission if mission is not None else []

    def serialize(self) -> str:
        """
        Takes a list of ScriptObject instances and returns a GMAT script string.
        """
        script_lines = []
        for resource in self.resources:
            # Serialize and append the object
            script_lines.append(resource.to_gmat_script())

        # Start the mission sequence
        script_lines.append("BeginMissionSequence;")
        for step in self.mission:           
            # Serialize and append the object
            script_lines.append(step.to_gmat_script())

        # Return the full script
        return "\n\n".join(script_lines).encode("ascii", errors="ignore").decode()

    @contextmanager
    def as_temp_file(self):
        import tempfile
        with tempfile.NamedTemporaryFile(suffix=".script", delete=False) as outfile:
            outfile.write(self.serialize().encode(encoding='ascii'))
            outfile.close()
            try:
                yield outfile.name
            finally:
                pass