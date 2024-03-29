import re

"""Konvertiert eine Textuelle Preis angabe in einen Float"""


def preis_zu_float(preis):
    return float(preis.replace("€", "").replace(",", ".").strip())


"""Konvertiert eine Url mit Element id in der Query zu der Element Id"""


def element_id_von_url(url):
    regex = re.compile("[0-9]{6,7}")
    match = re.search(regex, url)
    if match is not None:
        return url[match.regs[0][0]:match.regs[0][1]]
    else:
        return None

def set_id_von_url(url):
    regex = re.compile("[0-9]{4,5}")
    match = re.search(regex, url)
    if match is not None:
        return url[match.regs[0][0]:match.regs[0][1]]
    else:
        return None

def clean_setname(rawname):
    result = ""
    for i in rawname.split(" ")[1:-1]:
        result = result + i + " "
    return result.strip()

def clean_set_id(raw_set_id):
    return raw_set_id.split("-")[0]

def clean_line(line):
    try:
        return int(line.strip("x"))
    except Exception as e:
        zahl = ""
        for i in line:
            if i.isdigit():
                zahl += i
            elif i == 'x':
                break
        return int(zahl)







