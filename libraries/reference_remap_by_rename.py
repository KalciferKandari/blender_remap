# 2018_05_08_17_03_19

import bpy
from blender_remap.libraries.proj_path_utilities import to_blender_friendly_rel
from pathlib import PurePath
from blender_remap.libraries.reference_check_utilities import is_dupli_group_ref, \
    is_object_ref, is_material_ref


# ==========
# Reference remap by rename
# ==========
#
# ==========
# Description:
# ==========
# Remaps external references only.
#
# ==========
# Inputs:
# ==========
# - <string> abs_to_library: Absolute path to the original library.
# - <string> data_type: 'MESH', 'GROUP', 'MATERIAL'.
# - <string> old_data_name
# - <string> new_data_name
#
# ==========
# Return:
# ==========
# None.
#
# TODO Better error handling.
# TODO Test for DupliGroups.
# TODO Test for objects.
# TODO Test for materials.
def reference_remap_by_rename(abs_to_library, data_type, old_data_name,
                              new_data_name):
    print("----------")
    print("Now remapping external references.")
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
                if is_dupli_group_ref(obj_iter.dupli_group, old_data_name,
                                      library):
                    obj_iter.dupli_group.name = new_data_name
                    reference_found = True
                    break
        # ----------
        # If mesh.
        # ----------
        elif data_type == "MESH":
            for obj_iter in data.objects:
                if is_object_ref(obj_iter.data, old_data_name, library):
                    obj_iter.data.name = new_data_name
                    reference_found = True
                    break
        # ----------
        # If material.
        # ----------
        elif data_type == "MATERIAL":
            for mat_iter in data.materials:
                if is_material_ref(mat_iter, old_data_name, library):
                    mat_iter.name = new_data_name
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
        print("References were remapped.")
        print("----------")

        print("----------")
        print("Saving.")
        print("----------")
    else:
        print("----------")
        print("No references were remapped.")
        print("----------")

        bpy.ops.wm.save_mainfile()


if __name__ == "__main__":
    import sys

    # TODO
    # if "--" not in sys.argv:
    #     argv = []  # as if no args are passed
    # else:
    #     argv = sys.argv[sys.argv.index("--") + 1:]  # get all args after "--"

    reference_remap_by_rename(sys.argv[6], sys.argv[7], sys.argv[8],
                              sys.argv[9])
