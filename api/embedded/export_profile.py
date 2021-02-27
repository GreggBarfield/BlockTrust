import argparse
import os
import subprocess
import pathlib

# DO NOT AUTOMATE THIS SCRIPT! VULNERABILITIES EVERYWHERE!

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Prepares a folder that contains most of what is needed to run a profile."
    )

    # parser.add_argument('--profile', help='Profile name', type=str, required=True)

    args = parser.parse_args()

    p = "export_profile"  # + args.profile

    # Beware pycache

    subprocess.run(["mkdir", p])
    subprocess.run(["mkdir", os.path.join(p, "api")])
    subprocess.run(["cp", "api/embedded", os.path.join(p, "api", "embedded"), "-r"])
    subprocess.run(["cp", "api/client", os.path.join(p, "api", "client"), "-r"])
    [p.unlink() for p in pathlib.Path('.').rglob('*.py[co]')]
    [p.rmdir() for p in pathlib.Path(p).rglob('__pycache__')]
