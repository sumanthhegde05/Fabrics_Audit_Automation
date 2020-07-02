from openpyxl import Workbook, load_workbook
from contextlib import closing

def make_excel_file(file_name):
    with closing(Workbook()) as wb:
        wb.save(file_name)