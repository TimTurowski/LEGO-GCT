import re


def preis_zu_float(preis):
    return float(preis.replace("€", "").replace(",", ".").strip())

def element_id_von_url(url):
    regex = re.compile("[0-9]{6,7}")
    match = re.search(regex, url)
    if match!= None:
        return url[match.regs[0][0]:match.regs[0][1]]
    else:
        return None


