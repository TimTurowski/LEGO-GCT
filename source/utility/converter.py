

def preis_zu_float(preis):
    return float(preis.replace("€", "").replace(",", ".").strip())

