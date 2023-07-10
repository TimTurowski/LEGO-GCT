import re

"""prüft ob eine Id eine Gültige Element ID ist also aus 6 oder 7 Ziffern besteht"""


def is_valid_element_id(element_id):
    regex = re.compile("[0-9]{6,7}")
    return re.search(regex, element_id) is not None
