# 2018_05_08_22_08_08

from refactor.libraries.make_dupli_group_source import make_dupli_group_source

print("\n==========")
print("Script started.")
print("==========\n")


# ==========
# Make DupliGroup source
# ==========
#
# ==========
# Description:
# ==========
# Makes the selected DupliGroup the source by updating all the references to the old source.
#
# ==========
# Script usage:
# ==========
# - **Make a copy of the project folder, very important.**
# - Close all Blender windows, all of them.
# - Open the '.blend' file where the script will be run using 'blender file_name.blend'.
# - Link the script to the internal text editor.
# - Select the single DupliGroup to be made the source.
# - Make sure the DupliGroup has its transforms zeroed.
# - *The path must be correct, otherwise a lot of files could be ruined.*
# - Set the inputs where make_dupli_group_source() is called in the file. It takes an absolute path to the directory to be searched, and an absolute path the the script folder where this and the complementary scripts are stored.
# - Click 'Run Script' on the text editor panel.
# - Look at the console for errors.
# - Check the files to make sure they have integrity.
# - Can either archive the backup copy of the project or delete it now.
#
make_dupli_group_source(
    "ABSOLUTE_PATH",
    "ABSOLUTE_PATH"
)

print("\n==========")
print("Script finished.")
print("==========")
