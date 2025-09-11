import os
import subprocess
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
scripts = [f for f in os.listdir(current_dir) if f.endswith('.py') and f != 'all.py']

results = {}

for script in scripts:
    script_path = os.path.join(current_dir, script)
    print(f"Running {script}...")
    try:
        result = subprocess.run([sys.executable, script_path], cwd=current_dir, check=True)
        results[script] = "✅ Success"
    except subprocess.CalledProcessError as e:
        results[script] = f"❌ Failed (exit code {e.returncode})"
    except Exception as e:
        results[script] = f"❌ Failed (error: {e})"

# Summary
print("\n=== Script Execution Summary ===")
for script, status in results.items():
    print(f"{script}: {status}")
