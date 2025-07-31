import subprocess
import os

def get_idle_time():
    if os.environ.get("WAYLAND_DISPLAY"):
        print("Idle detection not supported on Wayland.")
        return 0

    try:
        output = subprocess.check_output(["xprintidle"])
        return int(output.strip())  # milliseconds
    except FileNotFoundError:
        print("Install xprintidle: sudo apt install xprintidle")
    except subprocess.CalledProcessError as e:
        print("xprintidle failed:", e)
    except Exception as e:
        print("Unknown idle error:", e)

    return 0
