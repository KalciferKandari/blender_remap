# 2018_05_08_15_57_38

import bpy
from blender_remap.libraries.blend_iterate import blend_iterate


# ==========
# Remap name
# ==========
#
# ==========
# Inputs:
# ==========
# - <string> new_name
# - <string> data_type: 'MESH', 'GROUP', 'MATERIAL'.
# - <string> project_path: Absolute project directory path to be recursively
#  searched for references to the library, and have their name changed.
# - <string> scripts_path: Absolute scripts directory path, where the
# accompanying scripts are stored.
#
# ==========
# Return:
# ==========
# None.
#
# TODO Better error handling.
#
def remap_name(new_name, data_type, project_path, scripts_path):
    # ----------
    # Variables.
    # ----------

    scene = bpy.context.scene
    data = bpy.data
    obj = scene.objects.active
    script_path = scripts_path + "\\" + "reference_remap_by_rename.py"
    err_name_exists = 'Exiting script: \'%s\' name "%s" already exists in ' \
                      'this file.' % (data_type, new_name)
    err_not_source = "Exiting script: This file must be the source of the " \
                     "data being renamed."

    # ----------

    # ----------
    # If group.
    # ----------
    if data_type == "GROUP":
        # ----------
        # Checks.
        # ----------

        # TODO Check if the current file is in the 'project_path'.

        if (obj.dupli_group is None) or (obj.dupli_type != "GROUP"):
            print(
                "Exiting script: In order to rename a group, a DupliGroup "
                "must be created to select it.")
            # Stop the script by returning.
            return

        # Check if the name is available in the current file.
        for group_iter in data.groups:
            if group_iter.name == new_name:
                print(err_name_exists)
                # Stop the script by returning.
                return

        if obj.dupli_group is None:
            print(
                "Exiting script: To rename a group, first create a local "
                "DupliGroup from it, and select that. The DupliGroup can be "
                "deleted after the script has been run.")
            # Stop the script by returning.
            return

        # Should it only work in the source file.
        if obj.dupli_group.library is not None:
            print(err_not_source)
            # Stop the script by returning.
            return

        # ----------

        old_name = obj.dupli_group.name

        # Renames the group and all the internally linked DupliGroups. No
        # need to iterate through all the DupliGroups directly.
        obj.dupli_group.name = new_name
    # ----------
    # If mesh.
    # ----------
    elif data_type == "MESH":
        # ----------
        # Checks.
        # ----------

        if obj.type != "MESH":
            print("Exiting script: Data not of type 'MESH'.")
            # Stop the script by returning.
            return
        elif obj.dupli_group is not None:  # TODO Does this work to ensure
            # that the data is of a mesh only?
            print(
                "Exiting script: The object data cannot have a DupliGroup "
                "associated with it.")
            # Stop the script by returning.
            return

        # Check if the name is available in the current file.
        for obj_iter in data.objects:  # TODO What if there is a fake mesh?
            if (obj_iter.data is not None) and (obj_iter.type == "MESH") and (
                    obj_iter.data.name == new_name):
                print(err_name_exists)
                # Stop the script by returning.
                return

        # Should it only work in the source file.
        if obj.data.library is not None:
            print(err_not_source)
            # Stop the script by returning.
            return

        # ----------

        old_name = obj.data.name

        # Renames the object data and all the internally linked objects. No
        # need to iterate through all the objects directly.
        obj.data.name = new_name
    # ----------
    # If material.
    # ----------
    elif data_type == "MATERIAL":
        # ----------
        # Checks.
        # ----------

        if obj.type != "MESH":
            print(
                "Exiting script: Selected object must be of type 'MESH' to "
                "change the name of a material.")
            # Stop the script by returning.
            return

        if obj.active_material is None:
            print("Exiting script: Selected object must have a material.")
            # Stop the script by returning.
            return

        # Check if the name is available in the current file.
        for mat_iter in data.materials:
            if mat_iter.name == new_name:
                print(err_name_exists)
                # Stop the script by returning.
                return

        # Should it only work in the source file.
        if obj.active_material.library is not None:
            print(err_not_source)
            # Stop the script by returning.
            return

        # ----------

        old_name = obj.active_material.name

        # Renames the material data and all the internally linked objects.
        # No need to iterate through all the objects directly.
        obj.active_material.name = new_name
    # ----------
    # If the data type given is not valid.
    # ----------
    else:
        print(
            "Exiting script: '%s' is not a valid data type for this "
            "function, which are 'MESH', 'GROUP', or 'MATERIAL'." % data_type)
        # Stop the script by returning.
        return

    print("----------")
    print("Remapped internal references.")

    # Update the scene just in case.
    bpy.context.scene.update()

    print("----------")
    print("Saving the current file.")

    bpy.ops.wm.save_mainfile()

    print("----------")
    print("Renaming external references.")

    # Rename external references by iterating through the '.blend' files in
    # the 'project_path'.
    blend_iterate(
        project_path,  # Direct argument.
        script_path,  # Direct argument.
        data.filepath,  # Argument to pass on.
        data_type,  # Argument to pass on.
        old_name,  # Argument to pass on.
        new_name  # Argument to pass on.
    )
