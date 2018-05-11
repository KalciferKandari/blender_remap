# 2018_05_08_22_13_21

from refactor.libraries.remap_name import remap_name

print("\n==========")
print("Script started.")
print("==========\n")


# ==========
# Remap name
# ==========
#
# ==========
# Description:
# ==========
# Renames some data and ensure all the internal and external links still work within a certain project directory.
#
# ==========
# Script usage:
# ==========
# - Make a copy of the project folder, very important.
# - Close all Blender windows, all of them.
# - Open the '.blend' file where the script will be run using 'blender file_name.blend'.
# - Do not mess-up the project path, that could be bad.
# - GROUP: Create DupliGroup in the source file, open the script in the internal text editor and type the new name for the first argument, 'GROUP' for the second argument, and the project path and script path for the next 2 arguments, run the script. The DupliGroup will remain, so deleted if you want.
# - MESH: Select the object in the source file, open the script in the internal text editor and type the new name for the first argument, 'MESH' for the second argument, and the project path and script path for the next 2 arguments, run the script.
# - MATERIAL: Select an object in the source file that has the material, select the material from the materials panel, open the script in the internal text editor and type the new name for the first argument, 'MATERIAL' for the second argument, and the project path and script path for the next 2 arguments, run the script.
#
remap_name(
    "NEW_NAME",  # New name.
    "DATA_TYPE",  # Data type of name: 'MESH', 'GROUP', 'MATERIAL'.
    "ABSOLUTE_PATH",  # Absolute project path.
    "ABSOLUTE_PATH")  # Absolute scripts path.

print("\n==========")
print("Script finished.")
print("==========")
