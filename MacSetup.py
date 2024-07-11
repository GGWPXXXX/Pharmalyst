import os
import subprocess

def create_and_activate_venv():
    os.system("python3 -m venv venv")
    activate_command = "source venv/bin/activate && pip install -r requirements.txt && python3 Monitor.py"
    subprocess.run(f"bash -c '{activate_command}'", shell=True)

if __name__ == "__main__":
    create_and_activate_venv()
