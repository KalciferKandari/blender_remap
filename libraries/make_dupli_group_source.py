# 2018_04_23_00_08_30

import bpy
from refactor.libraries.proj_path_utilities import abs_into_rel_to_proj, \
    rel_into_rel_to_proj
from refactor.libraries.link_external_group import link_external_group
from refactor.libraries.blend_iterate import blend_iterate


# ==========
# Make DupliGroup source.
# ==========
#
# ==========
# Inputs:
# ==========
# - <string> project_path: Absolute project directory path to be recursively
#  searched for references to the old library, and have them changed to the
# current '.blend' file.
# - <string> scripts_path: Absolute scripts directory path, where the
# accompanying scripts are stored.
#
# ==========
# Return:
# ==========
# None.
#
# TODO Make it work with more than one DupliGroup selected?
# TODO Better error handling.
def make_dupli_group_source(project_path, scripts_path):
    # TODO Add warning that the entire project should be backed-up before
    # running the script.

    # TODO Do all the libraries that are no longer necessary get garbage
    # collected properly?

    # TODO Check that all the transforms of the DupliGroup are zeroed.

    # ----------
    # Checks and variables.
    # ----------

    data = bpy.data
    scene = bpy.context.scene
    obj = scene.objects.active

    # TODO Check is project_path is valid.

    # Check if the active is an externally linked DupliGroup object.
    if (
            (obj.dupli_group is None)
            or (obj.dupli_type != "GROUP")
            or (obj.dupli_group.library is None)
    ):
        print(
            'Exiting script: The active object is not an externally linked '
            'DupliGroup.')
        # Stop the script by returning.
        return

    obj_dupligroup_name = obj.dupli_group.name
    obj_library = obj.dupli_group.library
    obj_library_path = obj_library.filepath
    current_file_rel_to_proj_path = abs_into_rel_to_proj(project_path,
                                                         data.filepath)
    script_path = scripts_path + "\\" + "reference_remap_by_relink.py"
    old_library_rel_to_proj_path = rel_into_rel_to_proj(
        current_file_rel_to_proj_path,
        obj_library_path)

    # Make sure the path is inside the project directory.
    if not old_library_rel_to_proj_path:
        print(
            "Exiting script: Can't have a path that is outside the project "
            "directory.")
        return

    # Check if the group name already exists and exit the script if it does.
    for group_iter in data.groups:
        if group_iter.name == obj_dupligroup_name:
            print(
                'Exiting script: Group "%s" already exists.' %
                obj_dupligroup_name)
            # Stop the script by returning.
            return

    # Go through the individual objects that are part of the DupliGroup and
    # check where their library is, if it is the old library, abort. We do
    # this because otherwise when changing internally linked DupliGroups in
    # the old library file to external, a circular reference would be
    # created, so the objects that have the circular references would not
    # turn up in the DupliGroups. This is the same even when linking
    # normally using the GUI. This is never a desirable outcome, so we stop
    # the script here.
    circulars = []
    for obj_iter in obj.dupli_group.objects:
        if (obj_iter.library.filepath == obj_library_path) and (
                not obj_iter.is_library_indirect):
            circulars.append("- '%s', of type '%s' in file '%s'." % (
                obj_iter.name, obj_iter.type, obj_iter.library.filepath))
    if circulars:
        print(
            "Exiting script: The following objects in this DupliGroup are "
            "local to the old library '.blend' file, which is at: %s. All the"
            " objects in the group in that file must be externally linked, "
            "otherwise circular references would be formed if there are "
            "internally linked DupliGroups in the old library, which would "
            "not appear correctly." % obj_library_path
        )
        for circular_iter in circulars:
            print(circular_iter)
        # Stop the script by returning.
        return

    # ----------

    # Delete obj.
    bpy.ops.object.delete()

    print("----------")
    print("Linking old source.")

    group_data = link_external_group(obj_library_path, obj_dupligroup_name)

    # ----------
    # Link the old source group to the scene.
    # ----------

    print("----------")
    print("Recreating group.")

    # No objects can be selected for the next part, so deselect all objects
    # just in case.
    for obj_iter in data.objects:
        obj_iter.select = False

    # Link the objects to the scene then make proxies of them by making
    # duplicate linked, and deleting the old ones.
    for obj_iter in group_data.objects:
        # Link the objects to the scene, it will not be possible to move them.
        linked_object = scene.objects.link(obj_iter)
        # Duplicate to a variable, not linked yet.
        duplicate_linked_obj = linked_object.object.copy()
        duplicate_linked_obj.data = linked_object.object.data.copy()  #
        # FIXME Is this necessary?
        # Delete the old object that could not be moved.
        data.objects.remove(linked_object.object, True)
        # Link the new proxy object.
        duplicate_linked_obj = scene.objects.link(duplicate_linked_obj)
        # Add to selection for grouping.
        duplicate_linked_obj.select = True

    # Create new group from the selected objects.
    bpy.ops.group.create(name=obj_dupligroup_name)

    # ----------

    # ----------
    # Remap references in this file from external to internal.
    # ----------

    # Find the local group. We need to do this because the group is not
    # returned by the operator function that creates it.
    print("----------")
    print("Remapping references in this '.blend' file.")

    local_group = None
    for group_iter in data.groups:
        if (group_iter.name == obj_dupligroup_name) and (
                group_iter.library is None):
            local_group = group_iter
            break

    number_of_remaps = 0

    # Make any old external links to the DupliGroup internal.
    # TODO Faster way to do this with library users_id?
    for obj_iter in data.objects:
        if (
                (obj_iter.dupli_group is not None)
                and (obj_iter.dupli_type == 'GROUP')
                and (obj_iter.dupli_group.name == obj_dupligroup_name)
                and (obj_iter.dupli_group.library == obj_library)
        ):
            obj_iter.dupli_group = local_group
            number_of_remaps += 1

    print("----------")
    print("Remapped " + str(number_of_remaps) + " internal references.")

    # ----------

    # Update the scene just in case.
    bpy.context.scene.update()

    print("----------")
    print("Saving the current file.")

    # Saving is necessary so the linking done in the other '.blend' files
    # actually works.
    bpy.ops.wm.save_mainfile()

    # ----------
    # Search for links to original.
    # ----------
    # Could have used blendfile.py, but instead chose to loop through
    # Blender files using an external Python script, because blendfile.py
    # didn't have any documentation or comments.

    print("----------")
    print("Remapping external references.")

    blend_iterate(
        project_path,  # Direct argument.
        script_path,  # Direct argument.
        project_path + '\\' + old_library_rel_to_proj_path,
        # Argument to pass on.
        data.filepath,  # Argument to pass on.
        "dupli_group",  # Argument to pass on.
        obj_dupligroup_name  # Argument to pass on.
    )

    # ----------
