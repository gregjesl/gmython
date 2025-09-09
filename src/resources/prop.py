from enum import Enum
from .resource import Resource
from .celestial import CelestialBody

class GravityField:
    def __init__(self, name: str, degree: int, order: int, file: str):
        self.name = name
        self.degree = degree
        self.order = order
        self.potential_file = file
        self.stm_limit = 100

    def to_gmat_script(self, model: str) -> str:
        return (
            f"GMAT {model}.GravityField.{self.name}.Degree = {self.degree};\n"
            f"GMAT {model}.GravityField.{self.name}.Order = {self.order};\n"
            f"GMAT {model}.GravityField.{self.name}.StmLimit = {self.stm_limit};\n"
            f"GMAT {model}.GravityField.{self.name}.PotentialFile = '{self.potential_file}';\n"
            f"GMAT {model}.GravityField.{self.name}.TideModel = 'None';"
        )
    
    """Generates a gravity field with the moon as the central body"""
    @staticmethod
    def moon(degree: int, order: int, file: str = "LP165P.cof"):
        return GravityField("Luna", degree, order, file)
    
    """Generates a gravity field with the Earth as the central body"""
    @staticmethod
    def earth(degree: int, order: int, file: str = "EGM96.cof"):
        return GravityField("Earth", degree, order, file)
    
class ErrorControl(Enum):
    RSSStep = 1
    RSSState = 2
    LargestStep = 3
    LargetsState = 4

class ForceModel(Resource):
    def __init__(self, name: str, gravity: GravityField, body: CelestialBody, point_masses: list[CelestialBody] = None):
        super().__init__(name)
        self.gravity_field = gravity
        self.body = body
        self.point_masses = point_masses if point_masses is not None else []
        self.error_control = ErrorControl.RSSStep

    def to_gmat_script(self) -> str:
        mass_names = []
        for mass in self.point_masses:
            mass_names.append(mass.name)
        point_masses_str = "{" + ", ".join(mass_names) + "}" if mass_names else "{}"
        script = (
            f"Create ForceModel {self.name};\n"
            f"GMAT {self.name}.CentralBody = {self.body.name};\n"
            f"GMAT {self.name}.PrimaryBodies = {{{self.body.name}}};\n"
            f"GMAT {self.name}.PointMasses = {point_masses_str};\n"
            f"GMAT {self.name}.Drag = None;\n"
            f"GMAT {self.name}.SRP = Off;\n"
            f"GMAT {self.name}.RelativisticCorrection = Off;\n"
            f"GMAT {self.name}.ErrorControl = {self.error_control.name};\n"
        )
        script += self.gravity_field.to_gmat_script(self.name)
        return script

class Propagator(Resource):
    def __init__(
        self,
        name: str,
        force_model: ForceModel,
    ):
        super().__init__(name)
        self.force_model_name = force_model.name
        self.method = "RungeKutta89"
        self.initial_step_size = 60.0
        self.accuracy = 1e-11
        self.min_step = 0.001
        self.max_step = 2700.0
        self.max_attempts = 50
        self.stop_if_violated = True

    def to_gmat_script(self) -> str:
        return (
            f"Create Propagator {self.name};\n"
            f"GMAT {self.name}.FM = {self.force_model_name};\n"
            f"GMAT {self.name}.Type = {self.method};\n"
            f"GMAT {self.name}.InitialStepSize = {self.initial_step_size};\n"
            f"GMAT {self.name}.Accuracy = {self.accuracy};\n"
            f"GMAT {self.name}.MinStep = {self.min_step};\n"
            f"GMAT {self.name}.MaxStep = {self.max_step};\n"
            f"GMAT {self.name}.MaxStepAttempts = {self.max_attempts};\n"
            f"GMAT {self.name}.StopIfAccuracyIsViolated = {'true' if self.stop_if_violated else 'false'};"
        )
