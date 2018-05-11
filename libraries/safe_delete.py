# 2018_05_08_22_04_25

import bpy
from refactor.libraries.blend_iterate import blend_iterate


# ==========
# Safe Delete
# ==========
#
# ==========
# Description:
# ==========
# Deletes a group, object, or material only if it has no references in a
# particular directory.
#
# ==========
# Usage:
# ==========
# Explained in main file.
#
# ==========
# Inputs:
# ==========
# - <string> data_type: 'MESH', 'GROUP', 'MATERIAL'.
# - <string> project_path: Absolute project directory path to be recursively
#  searched for references.
# - <string> scripts_path: Absolute scripts directory path, where the
# accompanying scripts are stored.
#
# ==========
# Return:
# ==========
# None.
#
def safe_delete(data_type, project_path, scripts_path):
    # ----------
    # Variables.
    # ----------

    scene = bpy.context.scene
    data = bpy.data
    obj = scene.objects.active
    script_path = scripts_path + "\\" + "reference_check.py"
    err_internal_reference_found = "Exiting script: Internal reference found."
    err_not_source = "Exiting script: This file must be the source of the " \
                     "data being renamed."
    dupli_group = None
    mat = None

    # ----------

    # ----------
    # If group.
    # ----------
    if data_type == "GROUP":
        # ----------
        # Checks.
        # ----------

        if (obj.dupli_group is None) or (obj.dupli_type != "GROUP"):
            print(
                "Exiting script: The selected object must be a DupliGroup of "
                "the group trying to be deleted, just so it can be selected.")
            # Stop the script by returning.
            return

        # Check for internal references.
        for obj_iter in data.objects:
            if (
                    (obj_iter.dupli_group is not None)
                    and (obj_iter.dupli_group == obj.dupli_group)
                    and (obj_iter != obj)
            ):
                print(err_internal_reference_found)
                # Stop the script by returning.
                return

        # Should it only work in the source file.
        if obj.dupli_group.library is not None:
            print(err_not_source)
            # Stop the script by returning.
            return

        # ----------

        name = obj.dupli_group.name
        dupli_group = obj.dupli_group
    # ----------
    # If mesh.
    # ----------
    elif data_type == "MESH":
        # ----------
        # Checks.
        # ----------

        # FIXME Need to determine whether this is the last user of a
        # material as well? Not going to do this right now because it would
        # require creating a batch version of 'reference_check.py'.

        if (obj.type != "MESH"):
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

        # Should it only work in the source file.
        if obj.data.library is not None:
            print(err_not_source)
            # Stop the script by returning.
            return

        # Check for internal references.
        for obj_iter in data.objects:  # TODO What if there is a fake mesh?
            if (obj_iter.data == obj.data) and (obj_iter != obj):
                print(err_internal_reference_found)
                # Stop the script by returning.
                return

        # ----------

        name = obj.data.name
    # ----------
    # If material.
    # ----------
    elif data_type == "MATERIAL":
        # ----------
        # Checks.
        # ----------

        mat = obj.active_material

        # Should it only work in the source file.
        if mat.library is not None:
            print(err_not_source)
            # Stop the script by returning.
            return

        # TODO Could use users_id to do this more quickly?
        # Check for internal references.
        for obj_iter in data.objects:
            if obj_iter != obj:
                for mat_iter in obj_iter.material_slots:
                    if mat_iter.material == mat:
                        print(err_internal_reference_found)
                        # Stop the script by returning.
                        return

        # ----------

        name = obj.active_material.name
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
    print("Checking for external references.")

    # Find external references by iterating through the '.blend' files in
    # the 'project_path'.
    return_codes = blend_iterate(
        project_path,  # Direct argument.
        script_path,  # Direct argument.
        data.filepath,  # Argument to pass on.
        data_type,  # Argument to pass on.
        name  # Argument to pass on.
    )

    # No references were found.
    for return_code_iter in return_codes:
        if return_code_iter == 1:
            print("----------")
            print("Reference was found, not deleting.")
            print("----------")
            break
    # References were found.
    else:
        if data_type == "GROUP":
            print("----------")
            print("Deleting group and the selected DupliGroup.")
            print("----------")
            data.groups.remove(dupli_group)
            # Also need to delete the selected object because it is a
            # DupliGroup that will lose its reference so definitely not
            # needed anymore.
            data.objects.remove(obj)
        elif data_type == "MESH":
            print("----------")
            print("Deleting selected object.")
            print("----------")
            data.objects.remove(obj)
        elif data_type == "MATERIAL":
            print("----------")
            print("Deleting selected material.")
            print("----------")

            # Not sure if the just the bottom of the two lines below is
            # necessary.
            data.materials.remove(mat)
            bpy.ops.object.material_slot_remove()
            pass

        # Update the scene just in case.
        bpy.context.scene.update()
