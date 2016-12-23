from copy import deepcopy

def first_of(pred, lst):
    for x in lst:
        if pred(x):
            return x

def index_of(pred, lst):
    for i, x in enumerate(lst):
        if pred(x):
            return i

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
