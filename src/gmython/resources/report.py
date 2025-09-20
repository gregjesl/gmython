import tempfile
import os
from contextlib import contextmanager
from pathlib import Path
from .resource import Resource
from .coordsys import CoordinateSystem

def cartesian_headers(obj: Resource, frame: CoordinateSystem) -> list[str]:
    return [
            f"{obj.name}.{frame.name}.X",
            f"{obj.name}.{frame.name}.Y",
            f"{obj.name}.{frame.name}.Z",
            f"{obj.name}.{frame.name}.VX",
            f"{obj.name}.{frame.name}.VY",
            f"{obj.name}.{frame.name}.VZ",
        ]

def keplerian_headers(obj: Resource, frame: CoordinateSystem) -> list[str]:
    return [
            f"{obj.name}.{frame.origin}.SMA",
            f"{obj.name}.{frame.origin}.ECC",
            f"{obj.name}.{frame.name}.INC",
            f"{obj.name}.{frame.name}.RAAN",
            f"{obj.name}.{frame.name}.AOP",
            f"{obj.name}.{frame.origin}.TA",
        ]

def spherical_headers(obj: Resource, frame: CoordinateSystem) -> list[str]:
    return [
            f"{obj.name}.{frame.origin}.RMAG",
            f"{obj.name}.{frame.origin}.Latitude",
            f"{obj.name}.{frame.origin}.Longitude",
        ]

def angular_momentum_headers(obj: Resource, frame: CoordinateSystem) -> list[str]:
    return [
            f"{obj.name}.{frame.origin}.HMAG",
            f"{obj.name}.{frame.name}.HX",
            f"{obj.name}.{frame.name}.HY",
            f"{obj.name}.{frame.name}.HZ",
        ]

class ReportResource(Resource):
    """Base class used for Report resource types"""
    pass

class ReportFile(ReportResource):
    def __init__(self, name, outfile: str, fields: list[str] | None = None, headers: bool = True, delimiter: str = " "):
        super().__init__(name)
        self.outfile = outfile
        self.fields = fields if fields is not None else []
        self.headers = headers
        self.delimiter = delimiter

    def to_gmat_script(self):
        def bool_to_gmat(val):
            return 'true' if val else 'false'

        lines = [
            f"Create ReportFile {self.name};",
            f"GMAT {self.name}.SolverIterations = Current;",
            f"GMAT {self.name}.RelativeZOrder = 0;",
            f"GMAT {self.name}.Maximized = false;",
            f"GMAT {self.name}.Filename = '{self.outfile}';",
            f"GMAT {self.name}.Precision = 16;",
            f"GMAT {self.name}.WriteHeaders = {bool_to_gmat(self.headers)};",
            f"GMAT {self.name}.LeftJustify = On;",
            f"GMAT {self.name}.ZeroFill = Off;",
            f"GMAT {self.name}.FixedWidth = true;",
            f"GMAT {self.name}.Delimiter = '{self.delimiter}';",
            f"GMAT {self.name}.ColumnWidth = 23;",
            f"GMAT {self.name}.WriteReport = true;"
        ]
        if self.fields:
            lines.append(f"GMAT {self.name}.Add = {{{', '.join(self.fields)}}};")
        return "\n".join(lines)

@contextmanager
def temp_report_file(fields: list[str] | None = None, headers: bool = True, delimiter: str = " "):
    with tempfile.NamedTemporaryFile(delete=False) as outfile:
        outfile.close()
        name = Path(outfile.name).stem
        try:
            yield ReportFile(name, outfile.name, fields, headers, delimiter)
        finally:
            pass

def parse_report(path: str) -> list[dict[str, float]]:
    data = []
    with open(path, 'r', encoding='ascii') as file:
        lines = file.readlines()
        if not lines:
            return data

        fields = lines[0].strip().split()
        for line in lines[1:]:
            values = line.strip().split()
            if len(values) != len(fields):
                raise ValueError(f"Row length mismatch: {values}")
            try:
                row = [float(value) for value in values]
            except ValueError as e:
                raise ValueError(f"Non-float value encountered: {e}")
            data.append(dict(zip(fields, row)))
    return data

class ReportReader(ReportResource):
    def __init__(self, name: str, file: str, fields: list[str] | None = None):
        super().__init__(name)
        self.fields = fields if fields is not None else []
        self.file = file

    def to_gmat_script(self):
        return ReportFile(self.name, self.file, self.fields, headers=True).to_gmat_script()

    def load(self) -> list[dict[str, float]]:
        return parse_report(self.file)
    
@contextmanager
def build_report_reader(fields: list[str] | None = None):
    with tempfile.NamedTemporaryFile(delete=False) as outfile:
        outfile.close()
        name = Path(outfile.name).stem
        try:
            yield ReportReader(name, outfile.name, fields)
        finally:
            pass