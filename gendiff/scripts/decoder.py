#!/usr/bin/env python3


def is_deep(node):
    keys_dicts = list(filter(lambda x: dict_or_list_checker(x, node), node))
    return True if keys_dicts else False


def dict_or_list_checker(element, node):
    if isinstance(node[element], dict) or isinstance(node[element], list):
        return element
    else:
        return False


def is_deep_with_list(node):
    if isinstance(node, dict):
        keys_dicts = list(filter(lambda x: isinstance(node[x], list), node))
    else:
        return False
    return True if keys_dicts else False


def dict_value(dictionary, level):
    result = '{'
    for key in dictionary:
        if not isinstance(dictionary[key], dict):
            exported_element = str(dictionary[key])
        else:
            exported_element = dict_value(dictionary[key], level + 1)

        result = result + '\n' + '    ' * (level + 1) + key + ": "\
            + exported_element

    result = result + '\n' + '    ' * level + "}"

    return result


def to_string(key, level, value, operator='common'):
    operators = {"common": '    ',
                 "0": '  - ',
                 "1": '  + '}

    lower_case_bool = {"True": "true",
                       "False": "false",
                       "null": "null"}
    if isinstance(value, bool):
        value = lower_case_bool.get(str(value))

    if isinstance(value, dict):
        value = dict_value(value, level)

    result = '    ' * (level - 1) + operators.get(operator)\
        + str(key) + ": " + str(value) + '\n'
    return result


def result_generator(pair, key, level, result):
    first_element, second_element = pair
    if first_element is None:
        result = result + to_string(key, level,
                                    second_element, str(1))
    elif second_element is None:
        result = result + to_string(key, level,
                                    first_element, str(0))
    else:
        result = result + to_string(key, level,
                                    first_element,
                                    str(0))
        result = result + to_string(key, level,
                                    second_element,
                                    str(1))
    return result


def stylish(dictionary):
    def inner(dictionary, result, level=1):
        for key in sorted(list(dictionary)):
            if isinstance(dictionary[key], dict) and is_deep(dictionary[key]):
                value = inner(dictionary[key], "", level + 1)
                result = result + to_string(key, level,
                                            value, 'common')
            elif isinstance(dictionary[key], list):
                result = result_generator(dictionary[key], key, level, result)
            else:
                result = result + to_string(key, level,
                                            dictionary[key], 'common')
        result = "{\n" + result + '    ' * (level - 1) + "}"
        return result
    return str('\n' + inner(dictionary, ''))


def plain_result(key, list_of_values):

    pair = list(map(lambda val:
                    '[complex value]' if isinstance(val, dict) else val,
                    list_of_values))

    bool_elements = {'True': 'true',
                     'False': 'false',
                     'null': 'null',
                     'None': 'None',
                     '[complex value]': '[complex value]'}
    pair = list(map(lambda val:
                    bool_elements.get(str(val))
                    if str(val) in bool_elements else str("'{}'".format(val)),
                    pair))

    template = '\nProperty \'{}\' was {}'
    added_element = ('added with value: {}').format(pair[1])
    updated_element = ('updated. From {} to {}').format(*pair)

    action_dict = {'1': 'removed',
                   '0': added_element,
                   '2': updated_element}
    result = ""

    index = 2
    for i in [0, 1]:
        if list_of_values[i] is None:
            index = i
            break

    action = action_dict.get(str(index))
    result = template.format(key, action)

    return result


def plain(dictionary):
    def inner(dictionary, result, parent):
        for key in sorted(list(dictionary)):
            if parent == '':
                parent_2 = key
            else:
                parent_2 = parent + "." + key

            added_line = ''
            if isinstance(dictionary[key], list):
                added_line = plain_result(parent_2, dictionary[key])
            if isinstance(dictionary[key], dict):
                added_line = inner(dictionary[key], '', parent_2)
            result = result + added_line

        return result
    return inner(dictionary, '', '')
