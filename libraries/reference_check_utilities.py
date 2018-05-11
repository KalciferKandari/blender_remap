# 2018_05_11_10_02_33


def is_dupli_group_ref(dupli_group, name, library):
    if (
            (dupli_group is not None)
            and (dupli_group.name == name)
            and (dupli_group.library == library)
    ):
        return True
    else:
        return False


def is_object_ref(obj_data, name, library):
    if (
            (obj_data is not None)
            and (obj_data.name == name)
            and (obj_data.library == library)
    ):
        return True
    else:
        return False


def is_material_ref(mat, name, library):
    if (
            (mat.name == name)
            and (mat.library == library)
    ):
        return True
    else:
        return False
