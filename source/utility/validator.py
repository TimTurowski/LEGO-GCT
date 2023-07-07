import re


def is_valid_element_id(element_id):
    regex = re.compile("[0-9]{6,7}")
    return re.search(regex, element_id) != None


