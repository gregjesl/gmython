from abc import ABC, abstractmethod
from enum import Enum
from contextlib import contextmanager
from .resources.resource import Resource
from .mission import MissionStep
from .resources.spacecraft import State, Epoch, TimeStandard, ModJulianEpoch, CoordinateSystem, EARTHMJ2000EQ, Spacecraft
from .resources.coordsys import CoordinateSystemAxes
from .resources.celestial import CelestialBody
from .resources.prop import ForceModel, Propagator
from .resources.burns import ImpulseiveBurn
from .resources.report import ReportResource
from .resources.variable import Variable
from .resources.solvers import DifferentialCorrector

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
    def __init__(self) -> None:
        self.resources = []
        self.mission = []
    
    def add_resource(self, resource: Resource) -> Resource:
        if not isinstance(resource, Resource):
            raise ValueError("Input is not a Resource")

        order = [
            Variable,
            CoordinateSystem,
            Spacecraft,
            ImpulseiveBurn,
            ForceModel,
            Propagator,
            DifferentialCorrector,
            ReportResource
        ]

        # Find the priority index based on inheritance
        try:
            resource_index = next(
                i for i, cls in enumerate(order) if isinstance(resource, cls)
            )
        except StopIteration:
            # If no match, append at the end
            raise TypeError(f"Resource type {type(resource).__name__} is not recognized in the ordering list")

        # Insert the resource into the list based on its priority in the `order` list
        for i, existing in enumerate(self.resources):
            try:
                # Determine the priority index of the existing resource in the list
                # This uses isinstance to support subclass matching
                existing_index = next(
                    j for j, cls in enumerate(order) if isinstance(existing, cls)
                )
            except StopIteration:
                # If the existing resource's type is not in the order list, skip it
                continue

            # If the existing resource has a lower priority (higher index),
            # insert the new resource before it
            if existing_index > resource_index:
                self.resources.insert(i, resource)
                return resource

        # If no lower-priority resource was found, append the new resource at the end
        self.resources.append(resource)
        return resource

    def set_mission(self, mission: list[MissionStep]):
        self.mission = mission

    @staticmethod
    def create(resources: list[Resource], mission: list[MissionStep] | None = None):
        result = Script()
        for resource in resources:
            result.add_resource(resource)
        if mission is not None:
            result.set_mission(mission)
        return result

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