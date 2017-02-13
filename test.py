import openpyxl
from copy import copy
from os import getcwd


book = openpyxl.load_workbook(filename='%s\\Накладная 2.xlsx' % (getcwd() + "\\templates\\order", ))


sheet = book['Отчет']


sheet.oddHeader.left.text = "Page &[Page] of &N"
sheet.oddHeader.left.size = 7


book.save('%s/%s' % ("C:\\Users\\Alexandr\\Desktop\\", "159753.xlsx"))