import source.utility.validator as validator
"""Die Klasse Einzelteil repräsentiert ein Lego Einzelteil mit Namen und Element id
der Name ist optional, da dieser nicht durch das Parsen gewonnen werden kann."""
class Einzelteil:

    def __init__(self, element_id, name="unnamed"):

        if not validator.is_valid_element_id(element_id):
            raise ValueError("Element Id muss aus 6 oder 7 Ziffern von 0-9 bestehen")
        self.__element_id = element_id
        self.__name = name

    @property
    def element_id(self):
        return self.__element_id

    @element_id.setter
    def element_id(self, new_element_id):

        if not validator.is_valid_element_id(new_element_id):
            raise ValueError("Element Id muss aus 6 oder 7 Ziffern von 0-9 bestehen")

        self.__element_id = new_element_id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__element_id == other.__element_id
        else:
            return False




