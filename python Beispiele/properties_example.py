from datetime import date

"""Beispiel für Klasse mit Properties"""


class Employee:
    def __init__(self, name, birth_date):
        self.name = name
        self.birth_date = birth_date

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value.upper()

    @property
    def birth_date(self):
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value):
        self._birth_date = date.fromisoformat(value)

    def __eq__(self, other):
        """isinstance prüft, ob die Objekte von derselben Klasse ist sonst funktioniert Equals ähnlich wie in Java"""
        if isinstance(other, self.__class__):
            return self.name == other._name and self.birth_date == other.birth_date
        else:
            return False

    def __str__(self):
        """str() sorgt dafür das __str__ von dem jeweiligen Objekt aufgerufen wird bei print geschieht dies implizit"""

        return "Name: " + self._name + " Geburtstag: " + str(self.birth_date)


person_1 = Employee("John", "2001-02-07")
print(person_1)
person_2 = Employee("Peter", "2001-02-07")
print(person_1 == person_2)
person_1.name = "Peter"
print(person_1 == person_2)

