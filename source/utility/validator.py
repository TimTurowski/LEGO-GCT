import re

"""prüft ob eine Id eine Gültige Element ID ist also aus 6 oder 7 Ziffern besteht"""


def is_valid_element_id(element_id):
    regex = re.compile("[0-9]{6,7}")
    return re.search(regex, element_id) is not None


"""prüft ob die bei der ToyPro angegebene Element Id mit der Such Id übereinstimmt und ob das gefundene
Element das Richtige ist"""
def is_correct_toypro_element(element_id, toypro_string):
    regex = re.compile("[0-9]{6,7}")
    match = re.search(regex, toypro_string)
    return match is not None and element_id == toypro_string[match.regs[0][0]:match.regs[0][1]]




