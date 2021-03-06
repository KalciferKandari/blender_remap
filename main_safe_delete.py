# 2018_05_10_11_27_01

from blender_remap.libraries.safe_delete import safe_delete

print("\n==========")
print("Script started.")
print("==========\n")

# ==========
# Safe delete
# ==========
#
# ==========
# Description:
# ==========
# Safely deletes data by ensuring there are no internal or external
# references to it within a project directory. Must be done in the source
# file of the data.
#
# - GROUP: Safely deletes a group, but not objects that were in it.
#     - **Note**: Those objects might still be part of other groups.
# - MESH: Safely deletes an object and its data.
#     - **Note** The object will still be deleted even if it is part of a
# group, but not if that group has DupliGroups created from it.
#     - **Note**: If the object being deleted is the last user of a
# material, that material will be deleted.
# - MATERIAL: Safely deletes a material and the material slot it was in.
#     - **Note**: If a material has been created in the current file and not
#  saved, it will be deleted even though if the file was saved it wouldn't be.
#
# ==========
# Script usage:
# ==========
#
# - **Make a copy of the project folder, very important.**
# - Close all Blender windows, all of them.
# - Use the command 'blender file_name.blend' to open the '.blend' file
# where the script will be run.
# - *The path must be correct, otherwise a lot of files could be ruined.*
# - GROUP:
#     - Create DupliGroup in the source file. This is just for the purpose
# of selecting the group.
#     - Open the script in the internal text editor.
#     - Set the inputs where safe_delete() is called in the file. It takes
# 'GROUP' for the first argument, and the project path and script path for
# the next 2 arguments, run the script.
#     - The DupliGroup will automatically be deleted.
# - MESH:
#     - Select the object in the source file.
#     - Open the script in the internal text editor.
#     - Set the inputs where safe_delete() is called in the file. It takes
# 'MESH' for the first argument, and the project path and script path for
# the next 2 arguments, run the script.
# - MATERIAL:
#     - Select an object in the source file that has the material.
#     - Select the material from the materials panel.
#     - Open the script in the internal text editor.
#     - Set the inputs where safe_delete() is called in the file. It takes
# 'MATERIAL' for the first argument, and the project path and script path
# for the next 2 arguments, run the script.
#
safe_delete(
    "DATA_TYPE",  # Data type of name: 'MESH', 'GROUP', 'MATERIAL'.
    "ABSOLUTE_PATH",  # Absolute project path.
    "ABSOLUTE_PATH")  # Absolute scripts path.

print("\n==========")
print("Script finished.")
print("==========")
