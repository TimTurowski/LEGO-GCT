import datetime

from source.datastructures.einzelteil import Einzelteil
from source.datastructures.einzelteil_marktpreis import EinzelTeilMarktpreis
def show_marktpreis_comparision(legolist, toyprolist):

    lego_element_ids = list(map(lambda n: n.einzelteil.element_id, legolist))
    toypro_element_ids = list(map(lambda n: n.einzelteil.element_id, toyprolist))

    element_ids = list(set(lego_element_ids) | set(toypro_element_ids))

    lego_dict = {}
    for i in legolist:
        lego_dict[i.einzelteil.element_id] = i.preis

    toypro_dict = {}
    for i in toyprolist:
        toypro_dict[i.einzelteil.element_id] = i.preis

    print("{:<11} {:<10} {:<10}".format("ElementId", "Lego Shop", "ToyPro"))
    for i in  element_ids:
        print("{:<11} {:<10} {:<10}".format(i, "{:4.2f}".format(lego_dict[i]) + " €", "{:4.2f}".format(toypro_dict[i]) + " €"))


