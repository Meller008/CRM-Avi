import barcode


def generate(cod):
    EAN = barcode.Code39(cod, add_checksum=False)
    EAN.save("temp/%s" % cod, options={'module_height': 5.0})
