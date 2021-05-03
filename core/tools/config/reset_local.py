from subprocess import run
import os


def reset_local():
    if (
        not os.path.exists("api") or
        not os.path.exists("core") or
        not os.path.exists("reports_worker/logistics.py") or
        not os.path.exists("core/renderers")
    ):
        print("Too messed up or bad working directory. Reset failed, exiting.")
        exit()

    run("rm local -rf")
    run("cp core/tools/config/developer_local_template local")


if __name__ == "__main__":
    print("Resetting...")
    reset_local()
    print("Reset.")
