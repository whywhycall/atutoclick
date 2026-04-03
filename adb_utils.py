import subprocess


def run_adb_command(cmd):
    try:
        result = subprocess.run(
            ["adb"] + cmd,
            capture_output=True,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return "", str(e)


def check_device():
    out, err = run_adb_command(["devices"])
    lines = out.splitlines()

    for line in lines[1:]:
        if "\tdevice" in line:
            return True, line.split("\t")[0]

    return False, None


def tap(x, y):
    return run_adb_command(["shell", "input", "tap", str(x), str(y)])


def swipe(x1, y1, x2, y2, duration=300):
    return run_adb_command([
        "shell", "input", "swipe",
        str(x1), str(y1), str(x2), str(y2), str(duration)
    ])


def launch_app(package_name):
    return run_adb_command([
        "shell", "monkey",
        "-p", package_name,
        "-c", "android.intent.category.LAUNCHER",
        "1"
    ])


def get_screen_size():
    out, err = run_adb_command(["shell", "wm", "size"])
    return out
