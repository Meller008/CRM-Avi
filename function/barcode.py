import barcode
from os import getcwd


def generate(cod):
    EAN = barcode.Code39(cod, add_checksum=False)
    EAN.save(getcwd() + "/temp/%s" % cod, options={'module_height': 7.0})
