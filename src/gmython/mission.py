from abc import abstractmethod
from .resources.prop import Propagator
from .resources.spacecraft import Spacecraft
from .resources.variable import Variable
from .resources.report import ReportFile, ReportReader
from .resources.celestial import CelestialBody
from .resources.solvers import DifferentialCorrector
from .resources.burns import ImpulseiveBurn
from enum import Enum

class Comparison(Enum):
    EQUAL = 1,
    LESS_THAN = 2,
    GREATER_THAN = 3

    def serialize(self) -> str:
        if self == Comparison.EQUAL:
            return "="
        elif self == Comparison.LESS_THAN:
            return "<"
        elif self == Comparison.GREATER_THAN:
            return ">"
        else:
            raise Exception("Unhandled comparison")

class Condition:
    def __init__(self, parameter: str, comparison: Comparison, value: float):
        self.parameter = parameter
        self.comparison = comparison
        self.value = value

    def serialize(self) -> str:
        return f"{self.parameter} {self.comparison.serialize()} {self.value}"
    
class MissionStep:
    def __init__(self, verb, description = "") -> None:
        self.verb = verb
        self.description = description

    @abstractmethod
    def to_gmat_script(self) -> str:
        pass

    def preamble(self) -> str:
        if self.description:
            return f"{self.verb} '{self.description}' "
        else:
            return f"{self.verb}"

class Propagate(MissionStep):
    def __init__(self, prop: Propagator, sats: list[Spacecraft], termination: list[tuple[str, float | None]], description = "") -> None:
        super().__init__("Propagate", description)
        self.prop = prop

        if not sats:
            raise ValueError("Must have at least one satellite to propagate") 
        self.sats = sats

        if not termination:
            raise ValueError("Must have at least one termination condition") 
        self.termination = termination
    
    def to_gmat_script(self) -> str:
        # Build the list of satellite names
        sat_names = []
        assert self.sats
        for sat in self.sats:
            sat_names.append(sat.name)
        sat_list = "(" + ", ".join(sat_names) + ")"

        # Build the termination list
        terms = []
        assert self.termination
        for term in self.termination:
            if term[1] is None:
                terms.append(f"{term[0]}")
            else:
                terms.append(f"{term[0]} = {term[1]}")
        term_list = ", ".join(terms)

        return f"{self.preamble()} {self.prop.name}{sat_list} {{{term_list}}}"

class Maneuver(MissionStep):
    def __init__(self,  burn: ImpulseiveBurn, spacecraft: Spacecraft, description = ""):
        super().__init__(description)
        self.burn = burn
        self.spacecraft = spacecraft

    def to_gmat_script(self):
        return f"Maneuver {self.burn.name}({self.spacecraft.name})"
        
class Report(MissionStep):
    """Reports variables"""
    def __init__(self, report: ReportFile | ReportReader, fields: list[str], description = ""):
        super().__init__("Report", description)
        self.report = report
        self.fields = fields

    def to_gmat_script(self):
        fields = " ".join(self.fields)
        return f"{self.preamble()} {self.report.name} {fields};"

class Stop(MissionStep):
    """Stops execution of the mission
    
    This is useful in control logic. It can be used to stop the mission if a certain criteria is met.    
    """
    def __init__(self):
        super().__init__("Stop")

    def to_gmat_script(self):
        return "Stop;"
    
STOP = Stop()
"""A constant instantiation of the Stop step"""

class MissionBlock:
    def __init__(self):
        self.contents = []

class MissionLogic(MissionStep):
    def __init__(self, open: str, contents: list[MissionStep] | None, close: str, description = ""):
        super().__init__(open, description)
        self.contents = contents if contents is not None else []
        self.close = close

    def to_gmat_script(self) -> str:
        result = [self.preamble()]
        for obj in self.contents:
            result.append(obj.to_gmat_script())
        result.append(self.close)
        return "\n".join(result)
    
    def append(self, contents: MissionStep):
        self.contents.append(contents)

class ForLoop(MissionLogic):
    def __init__(self, variable: Variable, start: int, step: int, end: int, contents: list[MissionStep] | None = None):
        super().__init__(f"For {variable.name} = {start}:{step}:{end};", contents, "EndFor;")

class WhileLoop(MissionLogic):
    def __init__(self, condition: Condition, contents: list[MissionStep] | None = None):
        super().__init__(f"While {condition.serialize()}", contents, "EndWhile;")
    
class IfBlock(MissionLogic):
    def __init__(self, condition: Condition, contents: list[MissionStep] | None = None):
        super().__init__(f"If {condition.serialize()}", contents, "EndIf;")

class SolverMode(Enum):
    RunInitialGuess = 1,
    Solve = 2

class ExitMode(Enum):
    DiscardAndContinue = 1,
    SaveAndContinue = 2,
    Stop = 3

class TargetBlock(MissionLogic):
    def __init__(self, solver: DifferentialCorrector, contents: list[MissionStep] | None = None, solvemode: SolverMode = SolverMode.Solve, exitmode: ExitMode = ExitMode.DiscardAndContinue, description = ""):
        open = f"Target {solver.name} {{SolveMode = {solvemode.name}, ExitMode = {exitmode.name}, ShowProgressWindow = false}};"
        super().__init__(open, contents, "EndTarget;", description)

class Vary(MissionStep):
    """Used in a Target block to specify what element to vary"""
    def __init__(self, solver: DifferentialCorrector, variable: str, initial = 0.5, perturbation = 0.0001, lower = -100, upper = 100, maxstep = 0.2, additivescale = 0.0, multiplescale = 1.0, description = ""):
        super().__init__(description)
        self.solver = solver
        self.variable = variable
        self.initial = initial
        self.perturbation = perturbation
        self.lower = lower
        self.upper = upper
        self.maxstep = maxstep
        self.additivescale = additivescale
        self.multiplescale = multiplescale

    def to_gmat_script(self):
        return f"Vary {self.solver.name}({self.variable} = {self.initial}, {{Perturbation = {self.perturbation}, Lower = {self.lower}, Upper = {self.upper}, AdditiveScaleFactor = {self.additivescale}, MultiplicativeScaleFactor = {self.multiplescale}}});"

class Achieve(MissionStep):
    """Used in a Target block to specify termination conditions"""
    def __init__(self, solver: DifferentialCorrector, goal: str, value, tolerance = 0.1, description: str = ""):
        super().__init__(description)
        self.solver = solver
        self.goal = goal
        self.value = value
        self.tolerance = tolerance

    def to_gmat_script(self):
        condition = Condition(self.goal, Comparison.EQUAL, self.value)
        return f"Achieve {self.solver.name}({condition.serialize()}, {{Tolerance = {self.tolerance}}});"
