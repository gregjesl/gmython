from resources.spacecraft import Spacecraft, KeplerianState
from resources.prop import GravityField, ForceModel, Propagator, CelestialBody
from mission import Propagate
from resources.coordsys import CoordinateSystem, CoordinateSystemAxes
from resources.celestial import EARTH, LUNA
from resources.report import keplerian_headers, build_report_reader
from dispatch import dispatch_instance, DispatchError
from script import Script

# Build the coordinate system
coordsys = CoordinateSystem("MoonMJ2000Eq", LUNA, CoordinateSystemAxes.MJ2000Eq)

# Build the satellite
state = KeplerianState(2000.0, 0.0, 45.0, 90.0, 135.0, 180.0)
sat = Spacecraft("Sat1", state, coord_system=coordsys)

# Build the force model
gravity = GravityField.moon(20, 20)
model = ForceModel("LunaForceModel", gravity, body=LUNA, point_masses=[EARTH])

# Build the propagator
prop = Propagator("DefaultProp", model)

# Build the report file
fields = ["Sat1.ElapsedSecs"] + keplerian_headers(sat, coordsys)

with build_report_reader(fields) as report:

    # Build the mission sequence
    mission = Propagate(prop, [sat], [("Sat1.ElapsedSecs", "12000.0")])

    # Build the script
    script = Script([coordsys, sat, model, prop, report], [mission])

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