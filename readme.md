<!-- 2018_05_11_17_52_31 -->

# Blender Remap

Project status: UNSTABLE. Not tested thoroughly, may still be serious issues.

## Introduction

3 Python scripts that are used for the purposes of refactoring library references, internal and external, in Blender project directories. The code works, but is quite primitive and slow.

They are designed to accompany [BAM Asset Manager](https://docs.blender.org/manual/en/dev/pipeline/bam.html), which allow the remapping of '.blend' files in a project directory, whereas these scripts allow the remapping of data within the '.blend' files themselves.

## Disclaimer

*I wrote these scripts for personal use only, so if you use them I accept no responsibility for the damages they may cause.*

*Backup before running any of these scripts.*

## The Scripts

**Backup the project directory before running any of these scripts** because it is searched recursively for '.blend' files and edits them. The error-checking isn't great, so something could go wrong and there is no way back.

### main_make_dulpi_group_source.py

Makes the selected DupliGroup the source, by converting the DupliGroup into a normal group while preserving the sub-DupliGroups, then updating all the references within a project directory.

#### Usage

- **Make a copy of the project folder, very important.**
- Close all Blender windows, all of them.
- Use the command 'blender file_name.blend' to open the '.blend' file where the script will be run.
- Link the script to the internal text editor.
- Select the single DupliGroup to be made the source.
- Make sure the DupliGroup has its transforms zeroed.
- *The path must be correct, otherwise a lot of files could be ruined.*
- Set the inputs where make_dupli_group_source() is called in the file. It takes an absolute path to the directory to be searched, and an absolute path the the script folder where this and the complementary scripts are stored.
- Click 'Run Script' on the text editor panel.
- Look at the console for errors.
- Check the files to make sure they have integrity.
- Can either archive the backup copy of the project or delete it now.

### main_remap_names.py

Renames the selected data and ensures all the internal and external links still work within a project directory.

#### Usage

- **Make a copy of the project folder, very important.**
- Close all Blender windows, all of them.
- Use the command 'blender file_name.blend' to open the '.blend' file where the script will be run.
- *The path must be correct, otherwise a lot of files could be ruined.*
- GROUP:
    - Create DupliGroup in the source file. This is just for the purpose of selecting the group.
    - Open the script in the internal text editor.
    - Set the inputs where remap_rename() is called in the file. It takes new name for the first argument, 'GROUP' for the second argument, and the project path and script path for the next 2 arguments.
    - Click 'Run Script' on the text editor panel.
- MESH:
    - Select the object in the source file.
    - Open the script in the internal text editor.
    - Set the inputs where remap_rename() is called in the file. It takes the new name for the first argument, 'MESH' for the second argument, and the project path and script path for the next 2 arguments.
    - Click 'Run Script' on the text editor panel.
- MATERIAL:
    - Select an object in the source file that has the material.
    - Select the material from the materials panel.
    - Open the script in the internal text editor.
    - Set the inputs where remap_rename() is called in the file. It takes the new name for the first argument, 'MATERIAL' for the second argument, and the project path and script path for the next 2 arguments.
    - Click 'Run Script' on the text editor panel.

### main_safe_delete.py

Safely deletes data by ensuring there are no internal or external references to it within a project directory. Must be done in the source file of the data.

- GROUP: Safely deletes a group, but not objects that were in it.
    - **Note**: Those objects might still be part of other groups.
- MESH: Safely deletes an object and its data.
    - **Note** The object will still be deleted even if it is part of a group, but not if that group has DupliGroups created from it.
    - **Note**: If the object being deleted is the last user of a material, that material will be deleted.
- MATERIAL: Safely deletes a material and the material slot it was in.
    - **Note**: If a material has been created in the current file and not saved, it will be deleted even though if the file was saved it wouldn't be.

#### Usage

- **Make a copy of the project folder, very important.**
- Close all Blender windows, all of them.
- Use the command 'blender file_name.blend' to open the '.blend' file where the script will be run.
- *The path must be correct, otherwise a lot of files could be ruined.*
- GROUP:
    - Create DupliGroup in the source file. This is just for the purpose of selecting the group.
    - Open the script in the internal text editor.
    - Set the inputs where safe_delete() is called in the file. It takes 'GROUP' for the first argument, and the project path and script path for the next 2 arguments, run the script.
    - The DupliGroup will automatically be deleted.
- MESH:
    - Select the object in the source file.
    - Open the script in the internal text editor.
    - Set the inputs where safe_delete() is called in the file. It takes 'MESH' for the first argument, and the project path and script path for the next 2 arguments, run the script.
- MATERIAL:
    - Select an object in the source file that has the material.
    - Select the material from the materials panel.
    - Open the script in the internal text editor.
    - Set the inputs where safe_delete() is called in the file. It takes 'MATERIAL' for the first argument, and the project path and script path for the next 2 arguments, run the script.

## Improvements

In the current form these scripts work for me, so I have no reason to spend a lot of time making them better, and if someone did I would even be very interested in switching to theirs.

Clearly the work-flow is not ideal, a lot of work could be done to improve the ease-of-use and speed that the scripts run.

- To begin with, iterating through the '.blend' files with the blender command is very slow, and in fact the scripts are a minute fraction that time, so the files should be read directly, possibly using [blendfile.py](https://github.com/scorpion81/blender-addons/blob/master/io_blend_utils/blend/blendfile.py).
- Of course a great improvement would be the conversion to a Blender add-on with a GUI, if possible.
- More robust error-handling. I didn't go into much detail into this. If the computer crashes part way through, for example, nothing is done to account for that. The only thing to do would be to restore the backup copy of the project directory.
- A lot of TODOs in the scripts give some ideas as to some improvements.
