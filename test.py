import barcode
from barcode import generate

EAN = barcode.Code39("088011", add_checksum=False)
ean = EAN.save("123")
