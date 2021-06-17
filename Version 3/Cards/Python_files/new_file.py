import xlsxwriter

def make_excel_file(file_name):
    print(file_name)
    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet()
    workbook.close()