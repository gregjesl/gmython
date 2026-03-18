from gmython.resources.report import build_report_reader
from gmython.dispatch import dispatch_instance, DispatchError
from gmython.script import Script
from gmython.resources.variable import Variable, Vector
from gmython.mission import ForLoop, Report, Assignment
from gmython import gmath

# Create a variable
angle = Variable("Angle")
vector = Vector.vector2("A")
xhat = Vector.vector2("xhat")
result = Variable("Result")

# Create a report reader
with build_report_reader() as report:

    # Create an empty loop
    loop = ForLoop(angle, 0, 45, 360)

    # Add a report step in the loop
    loop.append(Assignment(vector[1], gmath.cos(gmath.DegToRad(angle))))
    loop.append(Assignment(vector[2], gmath.sin(gmath.DegToRad(angle))))
    loop.append(Assignment(result, xhat.dot(vector)))
    loop.append(Report(report, [angle.name, result.name]))
    
    # Build the script
    script = Script.create([
        angle, 
        vector,
        xhat,
        result,
        report,
        Assignment(xhat[1], 1),
        Assignment(xhat[2], 0)
        ], [loop])

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