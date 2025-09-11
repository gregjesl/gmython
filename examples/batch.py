from gmython.resources.spacecraft import KeplerianState, Spacecraft
from gmython.resources.prop import GravityField, ForceModel, Propagator
from gmython.resources.celestial import LUNA, EARTH
from gmython.resources.coordsys import CoordinateSystem, CoordinateSystemAxes
from gmython.resources.report import keplerian_headers, build_report_reader
from gmython.mission import Propagate
from gmython.dispatch import dispatch_instance, DispatchError
from contextlib import ExitStack
from gmython.script import Script

# Build the coordinate system
coordsys = CoordinateSystem("MoonMJ2000Eq", LUNA, CoordinateSystemAxes.MJ2000Eq)

# Build the force model
gravity = GravityField.moon(20, 20)
model = ForceModel("LunaForceModel", gravity, body=LUNA, point_masses=[EARTH])

# Build the propagator
prop = Propagator("DefaultProp", model)

# Build the satellites
sats = []
for inc in range(90 + 1):
    state = KeplerianState(2000.0, 0.0, inc, 0.0, 0.0, 0.0)
    sat = Spacecraft("Sat1", state, coord_system=coordsys)
    sats.append(sat)

with ExitStack() as stack:
    # Build the report stack
    reports = [stack.enter_context(build_report_reader(["Sat1.ElapsedSecs"] + keplerian_headers(sat, coordsys))) for sat in sats]
    
    # Build the missions
    missions = []
    for sat, report in zip(sats, reports):

        # Build the mission sequence
        mission = Propagate(prop, [sat], [("Sat1.ElapsedSecs", 12000.0)])

        # Store the mission
        missions.append(Script([coordsys, sat, model, prop, report], [mission]))

    # Run the batch
    with dispatch_instance() as dispatch:
        try:
            dispatch.build_and_run_batch(missions)
        except DispatchError as e:
            with open(e.log) as log:
                print(log.read())

    # Print the last line in each report
    for report in reports:
        last = report.load()[-1]
        print(last)
