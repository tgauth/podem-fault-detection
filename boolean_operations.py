def inverse(boolean_value):
    """
    inverse function
    :param boolean_value: int, [0, 1, -1 (x)]
    :return: inverse of boolean_value, unless value
    is not yet initialized, then return -1
    """
    if boolean_value == 1:
        return 0
    elif boolean_value == 0:
        return 1
    else:
        return -1


def and_nand(var1, var2, not_flag=False):
    """
    and/nand function to handle 0, 1, D (2), D' (-2), and x (-1) inputs
    :param var1: int, first circuit input value
    :param var2: int, second circuit input value
    :param not_flag: boolean, true if NAND, false if AND
    :return:
    """
    # normal case
    if var1 in [0, 1] and var2 in [0, 1]:
        if not_flag:
            return inverse(var1 & var2)
        else:
            return var1 & var2
    # no defect propagated
    elif var1 == 0 or var2 == 0:
        if not_flag:
            return 1
        else:
            return 0
    # if either input is unknown then we don't know if defect will propagate
    elif var1 == -1 or var2 == -1:
        return -1
    elif var1 == -2 or var2 == -2:
        if var1 == -2 and var2 != 2 or var1 != 2 and var2 == -2:
            if not_flag:
                return 2
            else:
                return -2
        else:
            if not_flag:
                return 1
            else:
                return 0
    elif var1 == 2 or var2 == 2:
        if var1 == 2 and var2 != -2 or var1 != -2 and var2 == 2:
            if not_flag:
                return -2
            else:
                return 2
        else:
            if not_flag:
                return 1
            else:
                return 0


def or_nor(var1, var2, not_flag=False):
    """
    or/nor function to handle 0, 1, D (2), D' (-2), and x (-1) inputs
    :param var1: int, first circuit input value
    :param var2: int, second circuit input value
    :param not_flag: boolean, true if NOR, false if OR
    :return:
    """
    # normal case
    if var1 in [0, 1] and var2 in [0, 1]:
        if not_flag:
            return inverse(var1 | var2)
        else:
            return var1 | var2
    # no defect propagated
    elif var1 == 1 or var2 == 1:
        if not_flag:
            return 0
        else:
            return 1
    elif var1 == -1 or var2 == -1:
        return -1
    elif var1 == -2 or var2 == -2:
        if var1 == -2 and var2 != 2 or var1 != 2 and var2 == -2:
            if not_flag:
                return 2
            else:
                return -2
        else:
            if not_flag:
                return 0
            else:
                return 1
    elif var1 == 2 or var2 == 2:
        if var1 == 2 and var2 != -2 or var1 != -2 and var2 == 2:
            if not_flag:
                return -2
            else:
                return 2
        else:
            if not_flag:
                return 0
            else:
                return 1

