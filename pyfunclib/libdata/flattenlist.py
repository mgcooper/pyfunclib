
import functools
import operator

def flattenlist(nested_list):
    regular_list = []
    for ele in nested_list:
        if type(ele) is list:
            regular_list.append(ele)
        else:
            regular_list.append([ele])
    return regular_list

# might need to apply this:  functools.reduce(operator.iconcat, regular_list, []))