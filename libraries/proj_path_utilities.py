# 2018_05_02_06_14_59

from pathlib import PurePath
import os


# ==========
# Inputs:
# ==========
# - <string> project_path: The absolute project path.
# - <string> path: The absolute path to be made relative to 'project_path'
#
# ==========
# Return:
# ==========
# <string> The relative path.
#
def abs_into_rel_to_proj(project_path, path):
    # Return the relative path between 'path' and the common path between it
    #  and 'project_path'.
    return os.path.relpath(path, os.path.commonpath([project_path, path]))


# ==========
# Inputs:
# ==========
# - <string> relative_to_project_path: A path that is already relative to
# the project_path.
# - <string> path: A path that is relative to the first argument,
# relative_to_project_path.
#
# ==========
# Returns:
# ==========
# <string> or None.
#
# TODO Assumes that all the '..' in the 'path' argument are at the front.
# Might need to change this if it becomes a problem.
#
def rel_into_rel_to_proj(relative_to_project_path, path):
    p = PurePath(path)
    parts_1 = p.parts
    parts_2 = PurePath(relative_to_project_path).parts
    down = 0
    # Loop through the 2 path arguments and determine how much they go up
    # and down in order to find a common path factor.
    # TODO This does not account for symbolic links 'example/./path',
    # and maybe some other things, not sure if it will be a problem.
    for part in parts_1:
        if part == "..":
            down += 1
    return_path = PurePath('.')
    if down > len(parts_2) - 1:
        return
    else:
        depth = len(parts_2) - 1 - down
        counter = depth
        part_to_add = 0

        while counter is not 0:
            return_path = return_path.joinpath(parts_2[part_to_add])
            counter -= 1
            part_to_add += 1

        for counter, part in enumerate(parts_1):
            if (counter + 1) > down:
                return_path = return_path.joinpath(part)

        return str(return_path)


# ==========
# To Blender-friendly relative path.
# ==========
#
# ==========
# Description:
# ==========
# Makes an absolute path 'abs_path' relative to 'rel_to'. Both arguments
# should be absolute paths. It removes the './' or '.\' from the front.
#
def to_blender_friendly_rel(abs_path, rel_to):
    # Generate the relative path.
    rel_path = os.path.join(
        os.path.relpath(
            os.path.dirname(abs_path),
            os.path.dirname(rel_to)
        ),
        os.path.basename(abs_path)
    )
    # If there is a './' or '.\' at the front, remove it.
    rel_path = PurePath(rel_path)
    if (rel_path.parts[0] == '.\\') or (rel_path.parts[0] == './'):
        for counter, part_iter in enumerate(rel_path.parts):
            if counter > 0:
                rel_path = rel_path.joinpath(part_iter)
    else:
        rel_path = str(rel_path)

    return rel_path
