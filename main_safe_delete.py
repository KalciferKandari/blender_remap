# 2018_05_10_11_27_01

from refactor.libraries.safe_delete import safe_delete

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
# Safely deletes data by ensuring there are no internal or external references ot it. Must be done in the source file of the data.
#
# - GROUP: Safely deletes a group, but not objects that were in it.
# **Note**: That those objects might still be part of other groups.
# - MESH: Safely deletes an object and its data. Not that it will still be deleted even if it is part of a group, but not if that group has DupliGroups created from it.
# **Note**: If the object being deleted is the last user of a material, that material will be deleted.
# - Material : Safely deletes a material.
# **Note**: that if a material has been created in the current file and not saved, it will be deleted even though if the file was saved it wouldn't be.
#
# ==========
# Script usage:
# ==========
# - Make a copy of the project folder, very important.
# - Close all Blender windows, all of them.
# - Open the '.blend' file where the script will be run using 'blender file_name.blend'.
# - Do not mess-up the project path, that could be bad.
#
# - GROUP: Create DupliGroup in the source file, open the script in the internal text editor and type 'GROUP' for the first argument, and the project path and script path for the next 2 arguments, run the script. DupliGroup will be deleted.
#
# - MESH: Select the object in the source file, open the script in the internal text editor and type 'MESH' for the first argument, and the project path and script path for the next 2 arguments, run the script. The object and the mesh will be deleted.
#
# - MATERIAL: Select an object in the source file that has the material, select the material from the materials panel, open the script in the internal text editor and type 'MATERIAL' for the first argument, and the project path and script path for the next 2 arguments, run the script. The material and the slot it was in will be deleted.
#
safe_delete(
    "DATA_TYPE",  # Data type of name: 'MESH', 'GROUP', 'MATERIAL'.
    "ABSOLUTE_PATH",  # Absolute project path.
    "ABSOLUTE_PATH")  # Absolute scripts path.

print("\n==========")
print("Script finished.")
print("==========")
