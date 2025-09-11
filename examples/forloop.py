from gmython.resources.report import build_report_reader
from gmython.dispatch import dispatch_instance, DispatchError
from gmython.script import Script
from gmython.resources.variable import Variable
from gmython.mission import ForLoop, Report

# Create a variable
variable = Variable("I")

# Create a report reader
with build_report_reader() as report:

    # Create an empty loop
    loop = ForLoop(variable, 1, 1, 10)

    # Add a report step in the loop
    loop.append(Report(report, [variable.name]))
    
    # Build the script
    script = Script([variable, report], [loop])

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