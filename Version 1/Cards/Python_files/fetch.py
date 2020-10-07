import xlrd 
def extract(filename,column_no): 
    loc = filename
    test=[]
    wb = xlrd.open_workbook(loc) 
    sheet = wb.sheet_by_index(0) 
    sheet.cell_value(0, 0) 
    
    for i in range(sheet.nrows): 
        test.append(sheet.cell_value(i, int(column_no)))
    return test
