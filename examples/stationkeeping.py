from resources.spacecraft import Spacecraft, KeplerianState
from resources.prop import GravityField, ForceModel, Propagator, CelestialBody
from mission import Propagate, TargetBlock, Vary, Achieve, Maneuver, Report, ExitMode
from resources.coordsys import CoordinateSystem, CoordinateSystemAxes
from resources.celestial import EARTH, LUNA
from resources.report import keplerian_headers, build_report_reader
from resources.solvers import DifferentialCorrector
from resources.burns import ImpulseiveBurn, LocalCoordinateSystem, LocalCoordinateSystemAxes
from dispatch import dispatch_instance, DispatchError
from script import Script
import recipes

ALTITUDE = 50 # km
DEADBAND = 10 # km
INCLINATION = 45.0 # Degrees

# Build the coordinate system
coordsys = CoordinateSystem("MoonMJ2000Eq", LUNA, CoordinateSystemAxes.MJ2000Eq)

# Build the satellite
state = KeplerianState(LUNA.radius_of_altitude(ALTITUDE), 0.0, INCLINATION, 90.0, 135.0, 180.0)
sat = Spacecraft("Sat1", state, coord_system=coordsys)

# Build the force model
gravity = GravityField.moon(20, 20)
model = ForceModel("LunaForceModel", gravity, body=LUNA, point_masses=[EARTH])

# Build the propagator
prop = Propagator("DefaultProp", model)

# Build the differential corrector
dc = DifferentialCorrector("DC")

# Build the two maneuvers
lcs = LocalCoordinateSystem(LUNA, LocalCoordinateSystemAxes.VNB)
burns = [
    ImpulseiveBurn("PeriapsisBurn", lcs),
    ImpulseiveBurn("ApoapsisBurn", lcs)
]

with build_report_reader() as report:

    # Wrap up all of the resources
    resources = [
        coordsys,
        sat,
        model,
        prop,
        dc,
        burns[0],
        burns[1],
        report
    ]

    # Build the mission
    mission: list = [Propagate(prop, [sat], [(sat.relative_to(LUNA).rmag(), LUNA.radius_of_altitude(ALTITUDE - DEADBAND))], "Propagate Until Deadband Violation")]
    mission.append(recipes.propagate_to_periapsis(sat, prop, LUNA))

    # Build the targeting
    periapsis_target = TargetBlock(dc, exitmode=ExitMode.SaveAndContinue)
    periapsis_target.append(Vary(dc, burns[0].element1()))
    periapsis_target.append(Maneuver(burns[0], sat))
    periapsis_target.append(Achieve(dc, sat.relative_to(LUNA).apoapsis_radius(), LUNA.radius_of_altitude(ALTITUDE)))

    mission.append(periapsis_target)
    
    mission.append(recipes.propagate_to_apoapsis(sat, prop, LUNA))

    apoapsis_target = TargetBlock(dc, exitmode=ExitMode.SaveAndContinue)
    apoapsis_target.append(Vary(dc, burns[1].element1()))
    apoapsis_target.append(Maneuver(burns[1], sat))
    apoapsis_target.append(Achieve(dc, sat.relative_to(LUNA).sma(), LUNA.radius_of_altitude(ALTITUDE)))
    mission.append(apoapsis_target)
    
    mission.append(Report(report, ["Sat1.ElapsedDays", burns[0].element1(), burns[1].element1()]))

    # Build the script
    script = Script(resources, mission)

    with dispatch_instance() as dispatch:
        try:
            dispatch.build_and_run(script)
        except DispatchError as e:
            with open(e.log) as log:
                print(log.read())

    # Read out the report
    data = report.load()
    for line in data:
        print(line)