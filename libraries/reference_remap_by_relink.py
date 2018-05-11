# 2018_04_28_23_07_33

import bpy
from pathlib import PurePath
from refactor.libraries.link_external_group import link_external_group
from refactor.libraries.proj_path_utilities import to_blender_friendly_rel


# ==========
# Blend file reference remap.
# ==========
#
# ==========
# Description:
# ==========
# Meant to be run using the Blender command on the commandline.
# Searches through a '.blend' file and finds links to 'rel_to_old_library' or local links within the 'rel_to_old_library' file itself, then changes them to links to 'rel_to_new_libary'.
#
# ==========
# Inputs:
# ==========
# - <string> abs_to_old_library: An absolute path to the old library.
# - <string> abs_to_new_library: A absolute path to the new library.
# - <string> data_type: 'MESH', 'GROUP', 'MATERIAL'.
# - <string> data_name: Name of the object data from the libraries to be linked.
#
# ==========
# Return:
# ==========
# None.
#
def reference_remap_by_relink(abs_to_old_library, abs_to_new_library, data_type, data_name):
    # Using bpy.data.objects rather than scene.objects, because need to change the references of all the objects in the file, not just the current scene.
    data = bpy.data
    libraries = data.libraries
    rel_to_current_file = PurePath(data.filepath).name
    number_of_remaps = 0
    rel_to_old_library = '//' + to_blender_friendly_rel(abs_to_old_library, data.filepath)
    rel_to_new_library = '//' + to_blender_friendly_rel(abs_to_new_library, data.filepath)

    # ----------
    # If the current file is the old library, make the links to the DupliGroup external to the new library, rather than internal.
    # ----------
    if rel_to_current_file == rel_to_old_library:
        print("----------")
        print("This is the old library, now remapping internal references to external references.")
        print("----------")
        # Link the data from the new library.
        group_data = link_external_group(rel_to_new_library, data_name)
        # For every object in this '.blend' file.
        for obj_iter in data.objects:
            # If the object has a DupliGroup and is has the same name and is internal.
            if (
                    (obj_iter.dupli_group is not None)
                    and (obj_iter.dupli_group.name == data_name)
                    and (obj_iter.dupli_group.library is None)
            ):
                obj_iter.dupli_group = group_data
                number_of_remaps += 1
    # ----------
    # Don't need to check the new library file, because that is sorted in the main script.
    # ----------
    elif rel_to_current_file == rel_to_new_library:
        pass
    # ----------
    # If the current file is an external '.blend'.
    # ----------
    else:
        print("----------")
        print("Now remapping external references.")
        print("----------")
        # For every library.
        for library_iter in libraries:
            # If the library's file path is to the old library.
            if library_iter.filepath == (rel_to_old_library):
                # TODO The data is linked even if no DupliGroups are found, could check there are users before so don't waste time linking for no reason.
                # Link the data from the new library.
                group_data = link_external_group(rel_to_new_library, data_name)

                # TODO Faster way to do this with library users_id instead of looping through all the objects?
                # For every object in this '.blend' file.
                for obj_iter in data.objects:
                    # If the object has a DupliGroup and is has the same name and is external to the old library.
                    if (
                            (obj_iter.dupli_group is not None)
                            and (obj_iter.dupli_type == 'GROUP')
                            and (obj_iter.dupli_group.name == data_name)
                            and (obj_iter.dupli_group.library == library_iter)
                    ):
                        # Make link 'obj_iter' to data_to.groups[0]. TODO Does the following work? I think so.
                        obj_iter.dupli_group = group_data
                        number_of_remaps += 1

                break

    print("----------")
    print("Remapped " + str(number_of_remaps) + " references.")
    print("----------")

    if number_of_remaps > 0:
        print("----------")
        print("Saving.")
        print("----------")

        bpy.ops.wm.save_mainfile()


if __name__ == "__main__":
    import sys

    # TODO
    # if "--" not in sys.argv:
    #     argv = []  # as if no args are passed
    # else:
    #     argv = sys.argv[sys.argv.index("--") + 1:]  # get all args after "--"

    reference_remap_by_relink(sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9])
