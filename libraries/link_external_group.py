# 2018_05_06_12_11_30

import bpy


# ==========
# Link external group.
# ==========
#
# ==========
# Inputs:
# ==========
# - <string> library_path: Blender library path.
# - <string> group_name: Name of the group to be linked.
#
# ==========
# Return:
# ==========
# <bpy.types.Group> The group.
#
def link_external_group(library_path, group_name):
    # In this with statement, the data_to is just a list of strings, but after the with statement, it is actual data.
    with bpy.data.libraries.load(library_path, link=True) as (data_from, data_to):
        data_to.groups = [group_name]

    return data_to.groups[0]
