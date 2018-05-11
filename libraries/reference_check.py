# 2018_05_10_10_51_29

import bpy
from refactor.libraries.proj_path_utilities import to_blender_friendly_rel
from pathlib import PurePath
from refactor.libraries.reference_check_utilities import is_dupli_group_ref, \
    is_object_ref, is_material_ref


# ==========
# Reference check
# ==========
#
# ==========
# Description:
# ==========
# Checks a '.blend' file for a reference to data of name 'data_name' of
# type'data_type' that is externally linked to 'abs_to_library'.
#
# ==========
# Usage:
# ==========
# To be use with the Blender command, usually run using the Python
# subprocess.run() function.

# ==========
# Inputs:
# ==========
# - <string> abs_to_library: Absolute path to the original library.
# - <string> data_type: 'MESH', 'GROUP', 'MATERIAL'.
# - <string> data_name
#
# ==========
# Return:
# ==========
# None.
#
def reference_check(abs_to_library, data_type, data_name):
    print("----------")
    print("Now checking for external references.")
    print("----------")

    data = bpy.data
    rel_to_library = '//' + to_blender_friendly_rel(abs_to_library,
                                                    data.filepath)
    reference_found = False
    rel_to_current_file = PurePath(data.filepath).name
    library = None

    for library_iter in data.libraries:
        if library_iter.filepath == rel_to_library:
            library = library_iter
            break

    # ----------
    # Don't need to check the library file, because that is sorted in the
    # main script.
    # ----------
    if rel_to_current_file == rel_to_library:
        pass
    elif library is not None:
        # ----------
        # If group.
        # ----------
        if data_type == "GROUP":
            for obj_iter in data.objects:
                if is_dupli_group_ref(obj_iter.dupli_group, data_name,
                                      library):
                    reference_found = True
                    break
        # ----------
        # If mesh.
        # ----------
        elif data_type == "MESH":
            for obj_iter in data.objects:
                if is_object_ref(obj_iter.data, data_name, library):
                    reference_found = True
                    break
        # ----------
        # If material.
        # ----------
        elif data_type == "MATERIAL":
            for mat_iter in data.materials:
                if is_material_ref(mat_iter, data_name, library):
                    reference_found = True
                    break
        # ----------
        # If the data type given is not valid.
        # ----------
        else:
            print("----------")
            print(
                "'%s' is not a valid data type for this function, which are "
                "'MESH', 'GROUP', or 'MATERIAL'." % data_type)
            print("----------")
            return

    if reference_found:
        print("----------")
        print("Reference found.")
        print("----------")

        # This is how we communicate that there was a references. Not sure
        # if there is a better way.
        sys.exit(1)
    else:
        print("----------")
        print("No references found.")
        print("----------")


if __name__ == "__main__":
    import sys

    # TODO
    # if "--" not in sys.argv:
    #     argv = []  # as if no args are passed
    # else:
    #     argv = sys.argv[sys.argv.index("--") + 1:]  # get all args after "--"

    reference_check(sys.argv[6], sys.argv[7], sys.argv[8])
