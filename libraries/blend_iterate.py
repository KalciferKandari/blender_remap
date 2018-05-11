# 2018_04_28_22_22_53

from subprocess import run
from pathlib import Path


# ==========
# Blend file iterate.
# ==========
#
# ==========
# Description:
# ==========
# Recursively iterates through a directory and runs a script using the 'Blender' command on all the '.blend' files it finds.
#
# ==========
# Inputs:
# ==========
# - <string> project_path
# - <string> script_path
# - <string> <optional> script_argument
# - …
#
# ==========
# Return:
# ==========
# <list>[<float> or <int>] Return codes.
#
def blend_iterate(*args):
    print("----------")
    print("Starting blend_iterate().")

    project_path = args[0]
    script_path = args[1]
    script_arguments = []
    for counter, arg_iter in enumerate(args):
        if counter > 1:
            script_arguments.append(arg_iter)

    process_arguments = ["blender", "", "--background", "--python", script_path, "--"]
    for arg_iter in script_arguments:
        process_arguments.append(arg_iter)

    # Glob recursively searches the directory given to 'Path'.
    blend_paths = Path(project_path).glob('**/*.blend')

    return_codes = []
    # For every directory in the project_path, run the Blender command with the script
    for blend_path_iter in blend_paths:
        blend_path_iter = str(blend_path_iter)
        # 'blend_path_iter' is a 'Path' object, convert it to a string and assign it.
        process_arguments[1] = blend_path_iter

        print("----------")
        print("Searching through " + blend_path_iter)
        print("----------")

        return_code = run(process_arguments).returncode

        return_codes.append(return_code)

    print("----------")
    print("Ending blend_iterate().")
    print("----------")

    return return_codes


if __name__ == "__main__":
    import sys

    args = []
    for counter, argument in enumerate(sys.argv):
        if counter != 0:
            args.append(argument)

    blend_iterate(*args)
