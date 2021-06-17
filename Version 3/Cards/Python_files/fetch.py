import pandas as pd


def extract(filename,column_no): 
    print(filename)
    df = pd.ExcelFile(filename).parse(0)
    ret_list = df.iloc[:,int(column_no)].values.tolist()
    ret_list.insert(0,df.columns.values.tolist()[int(column_no)])
    return ret_list
