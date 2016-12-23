from copy import deepcopy

def head(lst):
    return lst[0] if len(lst) > 0 else None

def first_of(lst, x):
    return lst.index(x) if x in lst else None

def shuffle(lst, intgen):
    """
    Fisher-Yates shuffle implementation.
    lst: [t]
    intgen: int -> int -> int
    return: [t]

    """
    ret = deepcopy(lst)
    for i in range(len(ret) - 1):
        j = intgen(i, len(ret) - 1)
        ret[i], ret[j] = ret[j], ret[i]
    return ret
