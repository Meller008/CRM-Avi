import openpyxl
from copy import copy
from os import getcwd
import tempfile

t = tempfile.NamedTemporaryFile(dir=(getcwd() + "/temp/aaa.xlsx"))
print(t)


# book = openpyxl.load_workbook(filename='%s\\Накладная 2.xlsx' % (getcwd() + "\\templates\\order", ))
#
#
# sheet = book['Отчет']
#
#
# sheet.oddHeader.left.text = "Page &[Page] of &N"
# sheet.oddHeader.left.size = 7
#
#
# book.save(getcwd() + "/temp/")