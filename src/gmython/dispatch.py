import subprocess
import os
import tempfile
from contextlib import contextmanager
from .script import Script, ScriptObject

cmdlet = None

class DispatchError(Exception):
    def __init__(self, script: str | None, code: int, log: str):
        if script is None:
            super().__init__("GMAT returned " + str(code))
        else:
            super().__init__("Script " + script + " resulted in a return code of " + str(code))
        self.script = script
        self.log = log

class Dispatch:
    def __init__(self, logfile: str):
        if os.name == "nt":
            self.cmdlet = "GmatConsole.exe"
        elif os.name == "posix":
            self.cmdlet = "GmatConsole"

        if not os.path.exists(logfile):
            raise ValueError("Provided path too logfile is not valid")
        self.logfile = logfile
    
    def run(self, script: str):
        code = subprocess.run([self.cmdlet, "--verbose", "off", "--logfile", self.logfile, "--run", script], stdout=subprocess.DEVNULL).returncode
        if code != 0:
            raise DispatchError(script, code, self.logfile)
        
    def build_and_run(self, script: Script):
        with script.as_temp_file() as file:
            self.run(file)

    def batch(self, batch: str):
        # Run the batch file
        code = subprocess.run([self.cmdlet, "--verbose", "off", "--logfile", self.logfile, "--batch", batch], stdout=subprocess.DEVNULL).returncode

        # Check for errors
        if code != 0:
            raise DispatchError(None, code, self.logfile)
        
    def build_and_run_batch(self, scripts: list[Script]):
        from contextlib import ExitStack
        with ExitStack() as stack:
            files = [stack.enter_context(script.as_temp_file()) for script in scripts]
            with tempfile.NamedTemporaryFile(suffix=".batch", delete=False) as batch:
                for file in files:
                    batch.write((file + "\n").encode('ascii'))
                batch.close()
                self.batch(batch.name)

@contextmanager
def dispatch_instance():
    """Creates a temporary logfile and yields a dispatch instance"""
    with tempfile.NamedTemporaryFile(suffix=".log", delete=False) as logfile:
        logfile.close()
        try:
            yield Dispatch(logfile.name)
        finally:
            pass

def _batch_process(scripts: list[Script]):
    with dispatch_instance() as dispatch:
        dispatch.build_and_run_batch(scripts)

from multiprocessing import Pool

def parallel_process(missions: list[Script], threads: int | None = None):
    """
    Batch process a set of missions in parallel
    
    Warning
    -------
    main script must have `if __name__ == "__main__":`

    If it is not included in the main script, the process will not `fork()` correctly. 
    """
    if not missions:
        return

    if threads == 0:
        raise ValueError("Threads must be `None` or greater than zero")

    if threads is None:
        import os
        threads = os.cpu_count() or 1

    # Divide missions into roughly equal chunks
    def split_list(lst, n):
        k, m = divmod(len(lst), n)
        return [lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]

    blocks = split_list(missions, threads)

    with Pool(threads) as p:
        p.map(_batch_process, blocks)
