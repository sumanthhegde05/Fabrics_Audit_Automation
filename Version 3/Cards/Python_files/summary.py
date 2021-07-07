from re import A
import xlsxwriter
from openpyxl import Workbook
from contextlib import closing
import sys
import logging
import pandas as pd

"""
Notes:

CLass/Functions and its definition:

    1. make_excel_file(dir) --> None:
            Creates excel file in the directory dir.

    2. extract(filename,column_no) --> list:
            This function fetch data from the column_no of the filename provided. It returns the list of data from the specified column (0th row element to last entered row's element).

    3. ExcelUtility():
            Class provides objects to write into the excel files.
        
        a.  group(list,n) --> list:
                list elements are grouped into n elements and forms a list of list. Ex: [1,2,3,4,5,6,7,8] -> group(list,4) -> [[1,2,3,4][5,6,7,8]]

        b.  write_to_excel_file(filename,sheetname,content_list) --> None:
                Writes teh data into the particular sheetname of the filename. content_list is a list of data which is grouped into set of 4's. Group of 4 is now each element of the content_list representing row,column,value and format of the cell respectively.

                Formats:
                    False      = No format only border.
                    Bold       = Color:Black , Style:Bold , Background:None  
                    Red_Bold   = Color:Red , Style:Bold , Background:None 
                    Green_Bold = Color:Green , Style:Bold , Background:None 
                    Blue       = Color:Blue , Style:None , Background:None
                    Column0    = Color:Black , Style:Bold , Background:Purple
                    Column1    = Color:Black , Style:Bold , Background:Cyan
                    Header     = Color:Black , Style:Bold , Background:Yellow 
                    
    4. get_output_path() --> str:
            Returns the ouput path fecthed from the config file.
            
    5. create_output_files(output_path) --> str , str, str :
            Returns three strings containing input file name , summary file name and alternate summary file name respectively.
            
    6. def get_keywords() --> list, list, list: 
            Returns three lists containing search keywords, group name and group short name respectvely.
            
    7. def def get_logger() --> logger object:
            Creates and returns a logger object by defining its attributes.
            
    8. def add_to_summary_content() --> None:
            Method is used to add the data and its format to a specific row and column position.
"""




def make_excel_file(dir):
    with closing(Workbook()) as wb:
        wb.save(dir)


def extract(filename,column_no): 
    df = pd.ExcelFile(filename).parse(0)                    # df is a dataframe object. parse(0) indicates first sheet of the excel file.
    ret_list = df.iloc[:,int(column_no)].values.tolist()    # converting df object to list containing the data of specified column.
    ret_list.insert(0,df.columns.values.tolist()[int(column_no)])   #   inserting the table header data to the start of the list. (since df object excludes the header data) 
    return ret_list


class ExcelUtility():
    def __init__(self,value):           # Giving each object a value.
        self.value = value
    
    def group(self,lst, n):                                 # Grouping the list into set of four (row,column,value,format) to enter into excel.
        return zip(*[lst[i::n] for i in range(n)])          
    
    
    def write_to_excel_file(self,filename,sheetname,content_list):
        self.workbook = xlsxwriter.Workbook(filename)
        self.worksheet=[]
        self.sheetname=sheetname
        for i in range (0,len(sheetname)):
            self.worksheet.append(self.workbook.add_worksheet(sheetname[i]))
            if sheetname[i]=='input':                               # Setting the width of the column for different type of sheets.
                self.worksheet[i].set_column('A:A',20)
                self.worksheet[i].set_column('B:B',50)
                self.worksheet[i].set_column('C:J',20)
            elif self.value==0:
                self.worksheet[i].set_column('A:B', 50)
                self.worksheet[i].set_column('C:D',20)
                self.worksheet[i].set_column('E:E',40)
                self.worksheet[i].set_column('F:H',50)
                self.worksheet[i].set_column('I:I',20)
            else:
                self.worksheet[i].set_column('A:A', 50)
                self.worksheet[i].set_column('B:B', 20)
                self.worksheet[i].set_column('C:C', 50)
                self.worksheet[i].set_column('D:E',20)
                self.worksheet[i].set_column('F:F',40)
                self.worksheet[i].set_column('G:I',50)
                self.worksheet[i].set_column('J:J',20)
            
            self.cell_format = self.workbook.add_format({'align':'top', 'border':1 , 'border_color':'black'})
            self.cell_format.set_text_wrap()
        
            self.bold = self.workbook.add_format({'bold': True , 'align':'top' , 'align':'center' , 'bg_color':'yellow' , 'font_size':14 , 'border':2 , 'border_color':'black'})
            self.bold.set_text_wrap()
            
            self.redbold=self.workbook.add_format({'bold': True, 'font_color': 'red', 'align':'top', 'border':1 , 'border_color':'black'})
            self.redbold.set_text_wrap()
            
            self.greenbold=self.workbook.add_format({'bold': True, 'font_color': 'green', 'align':'top', 'border':1 , 'border_color':'black'})
            self.greenbold.set_text_wrap()
            
            self.blue=self.workbook.add_format({'font_color': 'blue', 'align':'top', 'border':1 , 'border_color':'black'})
            self.blue.set_text_wrap()
            
            self.column0=self.workbook.add_format({'bold': True, 'align':'left' , 'align':'vcenter' , 'bg_color':'#b19cd9', 'border':1 , 'border_color':'black' , 'font_size': 12})
            self.column0.set_text_wrap()
            
            self.column1=self.workbook.add_format({'bold': True, 'align':'left' , 'align':'vcenter' , 'bg_color':'cyan', 'border':1 , 'border_color':'black' , 'font_size': 12})
            self.column1.set_text_wrap()
            
            self.Head=self.workbook.add_format({'bold': True, 'align':'left' , 'align':'vcenter' , 'bg_color':'#7CFC00', 'border':1 , 'border_color':'black' , 'font_size': 12})
            self.Head.set_text_wrap()
            
            temp = self.group(content_list[i],4)
            
            for item in temp:
                try:
                    if item[3]==False:
                        self.worksheet[i].write(int(item[0]), int(item[1]), item[2],self.cell_format)
                    if item[3]=='Bold':
                        self.worksheet[i].write(int(item[0]), int(item[1]), item[2],self.bold)
                    elif item[3]=='Red_Bold':
                        self.worksheet[i].write(int(item[0]), int(item[1]), item[2],self.redbold)
                    elif item[3]=='Green_Bold':
                        self.worksheet[i].write(int(item[0]), int(item[1]), item[2],self.greenbold)
                    elif item[3]=='Blue':
                        self.worksheet[i].write(int(item[0]), int(item[1]), item[2],self.blue)
                    elif item[3]=='Column1':
                        self.worksheet[i].write(int(item[0]), int(item[1]), item[2],self.column1)
                    elif item[3]=='Column0':
                        self.worksheet[i].write(int(item[0]), int(item[1]), item[2],self.column0)
                    elif item[3]=='Header':
                        self.worksheet[i].write(int(item[0]), int(item[1]), item[2],self.Head)
                except:
                    print("error",item)
                    
        self.workbook.close()               # Saves the entire work
        

def get_output_path():                  # Fetching the output path from the config file
    file = open('config.txt')
    data=[]
    inc=-1

    for each in file:
        inc+=1
        word = each.split()
        data.append([])
        for item in word:
            data[inc].append(item)
            
    if data[inc][0]=='output_path=':
        return data[inc][1]
    

def create_output_files(output_path):   # Creating output summary files.
    input_file                  =   output_path+'\\Audit_'+sys.argv[2]+'\\Audit_report_unique_'+sys.argv[2]+'.xlsx'                 # Input file will be the consolidated sheet.
    summary_output_file         =   output_path+'\\Audit_'+sys.argv[2]+'\\Audit_report_summary_'+sys.argv[2]+'.xlsx'                # Audit_report_summary contains the data sorted as per the part numbers/sheet.
    alt_summary_output_file     =   output_path+'\\Audit_'+sys.argv[2]+'\\Audit_report_summary_alternate_'+sys.argv[2]+'.xlsx'      # Audit_report_summary_alternate contains the data stored as per the group name/sheet.
    make_excel_file(summary_output_file)
    make_excel_file(alt_summary_output_file)
    return input_file, summary_output_file, alt_summary_output_file


def get_keywords():                     # Fetching keywords from the keywords excel file.
    search = extract('keywords.xlsx',0)     # list of  keyword for the respective grups
    group = extract('keywords.xlsx',1)      # list of group names 
    short_group = extract('keywords.xlsx',2)    # list of short names for the group (short name is required because the sheet name in excel has word limit.)
    return search, group, short_group           


def get_logger():                       # Method to create a logger object which is used to generate debug logs.
    logger = logging.getLogger(__name__)    # setting a name="script name" to the logger object.
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler("debug_main.log",mode='a')                                               # creating a file handler.
    file_handler.setLevel(logging.DEBUG)                                                                        # Handler level is set to DEBUG so that all the entries are made to the debug file.
    file_handler.setFormatter(logging.Formatter('%(name)s : %(levelname)-8s : %(lineno)s : %(message)s'))       # Entry format
    console_handler = logging.StreamHandler(sys.stdout)                                                         # Creating a console handler to display the ouput in the console.
    console_handler.setLevel(logging.INFO)                                                                      # level is set to info so that only INFO and higher level messages are diplayed. (debug messages are excluded).
    console_handler.setFormatter(logging.Formatter('%(message)s'))                                              # Dislpay format
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    return logger



def add_to_summary_content(row,column,value,format):       # method to add to the global list of contents 
    global summary_content
    summary_content[-1].append(row)         # row-column =>  of the cell
    summary_content[-1].append(column)
    summary_content[-1].append(value)       # Value to be filled in the cell
    summary_content[-1].append(format)      # Format of the cell


def summary():
    global summary_content
    
    for item in range (1,len(Input_part_numbers)):
        summary_content.append([])
        
        inc=0
        add_to_summary_content(inc,0,Input_part_numbers[item],'Header')
        add_to_summary_content(inc,1,Card_name[item],'Header')
        
        inc+=1
        add_to_summary_content(inc,0,'Group Name','Bold')
        add_to_summary_content(inc,1,'Product Name','Bold')
        add_to_summary_content(inc,2,'Date','Bold')
        add_to_summary_content(inc,3,'Version','Bold')
        add_to_summary_content(inc,4,'OS','Bold')
        add_to_summary_content(inc,5,'File name','Bold')
        add_to_summary_content(inc,6,'Download_URL','Bold')
        add_to_summary_content(inc,7,'Description','Bold')
        add_to_summary_content(inc,8,'Severity','Bold')
        
        for i in range (1,len(group_names)):    # Iterating through list of data fetched from the keyword xlsx.
            group_name_flag=True                # Flag used to keep track of the elements that come under the same group.
            condition_status_check=False        # Flag used to check weather the group of card are supported for the partcular part numer or not.
            
            for j in range (1,len(Product_name)):   # Itereatig through list of products fetched from the unique report.
                
                if group_names[i]=='Mellanox OFED 4.x' and OFED4_support[item]=='NO':
                    condition_status_check=True
                    break
                
                if group_names[i]=='Mellanox OFED 5.x' and OFED5_support[item]=='NO':
                    condition_status_check=True
                    break
                
                elif group_names[i]=='WinOF' and WinOF_support[item]=='NO' :
                    condition_status_check=True
                    break
                elif group_names[i]=='WinOF2' and WinOF2_support[item]=='NO':
                    condition_status_check=True
                    break
                elif 'Mellanox MFT' in group_names[i] and MFT_support[item]=='NO':
                    condition_status_check=True
                    break            
                elif 'ESXi' in group_names[i] and VM_support[item]=='NO':
                    condition_status_check=True
                    break
                elif 'Windows firmware' in group_names[i] and Windows_fw_support[item]=='NO':
                    condition_status_check=True
                    break
                elif 'Linux RoCE' in group_names[i] and Linux_RoCE_support[item]=='NO':
                    condition_status_check=True
                    break
                elif 'Firmware binary' in group_names[i] and FW_binary_support[item]=='NO':
                    condition_status_check=True
                    break
                
                elif 'FWPKG' in group_names[i] and FWPKG_support[item]=='NO':
                    condition_status_check=True
                    break
                
                
                
                elif search_elem[i] in str(File_name[j]) and Input_part_numbers[item]==Part_numbers[j]:
                    inc+=1 
                    if group_name_flag==True:
                        add_to_summary_content(inc,0,group_names[i],'Column1')
                        group_name_flag=False
                    else:
                        add_to_summary_content(inc,0,'','Column1')
                        
                    add_to_summary_content(inc,1,Product_name[j],False)
                    add_to_summary_content(inc,2,Date[j],False)
                    add_to_summary_content(inc,3,Version[j],False)
                    add_to_summary_content(inc,4,Os[j],False)
                    add_to_summary_content(inc,5,File_name[j],False)
                    add_to_summary_content(inc,6,Download_url[j],False)
                    add_to_summary_content(inc,7,Description[j],False)
                    add_to_summary_content(inc,8,Severity[j],False)
                
                elif search_elem[i] in Product_name[j] and Input_part_numbers[item]==Part_numbers[j]:
                    
                    inc+=1 
                    if group_name_flag==True:
                        add_to_summary_content(inc,0,group_names[i],'Column1')
                        group_name_flag=False
                    else:
                        add_to_summary_content(inc,0,'','Column1')
                        
                    
                    
                        
                    
                    
                    if Input_part_numbers[item].strip() not in Product_name[j] :            # To check weather the part number is matching with the product name
                        
                        if group_names[i]=='Firmware binary posting':                       # Only for FW Binary postings.
                            add_to_summary_content(inc,1,Product_name[j],'Blue')       # If there is no match highlight with blue colour

                        else:
                            add_to_summary_content(inc,1,Product_name[j],False)       
                            
                    else:
                        add_to_summary_content(inc,1,Product_name[j],False)
                        
                    
                    
                    add_to_summary_content(inc,2,Date[j],False)
                    add_to_summary_content(inc,3,Version[j],False)
                    add_to_summary_content(inc,4,Os[j],False)
                    
                                    
                    if File_name[j]=='Not Found':
                        add_to_summary_content(inc,5,File_name[j],'Red_Bold')      # Making 'File not found' as Red Bold characters.
                    else:
                        add_to_summary_content(inc,5,File_name[j],False)
                    
                    add_to_summary_content(inc,6,Download_url[j],False)
                    add_to_summary_content(inc,7,Description[j],False)
                    add_to_summary_content(inc,8,Severity[j],False)
                    
                    
                    
        
            if group_name_flag==True:
                inc+=1
                add_to_summary_content(inc,0,group_names[i],'Column1')
                
            
                if condition_status_check==True:                    # If it is true then the respective group is not supported by the card according to the input file.
                    add_to_summary_content(inc,1,'Not Supported','Green_Bold')
                    condition_status_check=False
                    
                elif group_names[i]=='Firmware binary posting':     # If it is Flase then the group is supported by the card but there was no product found.
                    add_to_summary_content(inc,1,'No firmware posting for '+Input_part_numbers[item-1]+' found','Red_Bold')
                else:
                    add_to_summary_content(inc,1,'No Products Found','Red_Bold')
                
                add_to_summary_content(inc,2,' ',False)
                add_to_summary_content(inc,3,' ',False)
                add_to_summary_content(inc,4,' ',False)
                add_to_summary_content(inc,5,' ',False)
                add_to_summary_content(inc,6,' ',False)
                add_to_summary_content(inc,7,' ',False)
                add_to_summary_content(inc,8,' ',False)


def add_to_alt_summary_content(row,column,value,format):
    global alt_summary_content
    alt_summary_content[-1].append(row)
    alt_summary_content[-1].append(column)
    alt_summary_content[-1].append(value)
    alt_summary_content[-1].append(format)
    

def summary_alt():
    global alt_summary_content
    
    for item in range (1,len(group_names)):
        alt_summary_content.append([])
        
        inc=0
        add_to_alt_summary_content(inc,0,group_names[item],'Header')
    
        inc+=1
        add_to_alt_summary_content(inc,0,'Card Name','Bold')
        add_to_alt_summary_content(inc,1,'Part Number','Bold')
        add_to_alt_summary_content(inc,2,'Product Name','Bold')
        add_to_alt_summary_content(inc,3,'Date','Bold')
        add_to_alt_summary_content(inc,4,'Version','Bold')
        add_to_alt_summary_content(inc,5,'OS','Bold')
        add_to_alt_summary_content(inc,6,'File Name','Bold')
        add_to_alt_summary_content(inc,7,'Download_URL','Bold')
        add_to_alt_summary_content(inc,8,'Description','Bold')
        add_to_alt_summary_content(inc,9,'Severity','Bold')
        
        for i in range (1,len(Input_part_numbers)):
            group_name_flag=True
            condition_status_check=False
            
            for j in range (1,len(Product_name)):
                    
                if group_names[item]=='Mellanox OFED 4.x' and OFED4_support[i]=='NO':
                    condition_status_check=True
                    break
                
                if group_names[item]=='Mellanox OFED 5.x' and OFED5_support[i]=='NO':
                    condition_status_check=True
                    break
                
                elif group_names[item]=='WinOF' and WinOF_support[i]=='NO' :
                    condition_status_check=True
                    break
                elif group_names[item]=='WinOF2' and WinOF2_support[i]=='NO':
                    condition_status_check=True
                    break
                elif 'Mellanox MFT' in group_names[item] and MFT_support[i]=='NO':
                    condition_status_check=True
                    break            
                elif 'ESXi' in group_names[item] and VM_support[i]=='NO':
                    condition_status_check=True
                    break
                elif 'Windows firmware' in group_names[item] and Windows_fw_support[i]=='NO':
                    condition_status_check=True
                    break
                elif 'Linux RoCE' in group_names[item] and Linux_RoCE_support[i]=='NO':
                    condition_status_check=True
                    break
                elif 'Firmware binary' in group_names[item] and FW_binary_support[i]=='NO':
                    condition_status_check=True
                    break
                
                elif 'FWPKG' in group_names[item] and FWPKG_support[i]=='NO':
                    condition_status_check=True
                    break
                
                
                elif search_elem[item] in str(File_name[j]) and Input_part_numbers[i]==Part_numbers[j]:
                    inc+=1 
                    if group_name_flag==True:
                        add_to_alt_summary_content(inc,0,Card_name[i],'Column0')
                        add_to_alt_summary_content(inc,1,Input_part_numbers[i],'Column1')
                        group_name_flag=False
                    else:
                        add_to_alt_summary_content(inc,0,' ','Column0')
                        add_to_alt_summary_content(inc,1,' ','Column1')
                        
                    add_to_alt_summary_content(inc,2,Product_name[j],False)
                    add_to_alt_summary_content(inc,3,Date[j],False)
                    add_to_alt_summary_content(inc,4,Version[j],False)
                    add_to_alt_summary_content(inc,5,Os[j],False)
                    add_to_alt_summary_content(inc,6,File_name[j],False)
                    add_to_alt_summary_content(inc,7,Download_url[j],False)
                    add_to_alt_summary_content(inc,8,Description[j],False)
                    add_to_alt_summary_content(inc,9,Severity[j],False)
                    
                
                elif search_elem[item] in Product_name[j] and Input_part_numbers[i]==Part_numbers[j]:
                    inc+=1 
                
                
                
                    
                    if group_name_flag==True:
                        add_to_alt_summary_content(inc,0,Card_name[i],'Column0')
                        add_to_alt_summary_content(inc,1,Input_part_numbers[i],'Column1')
                        group_name_flag=False
                    else:
                        add_to_alt_summary_content(inc,0,' ','Column0')
                        add_to_alt_summary_content(inc,1,' ','Column1')
                        
                        
                    if Input_part_numbers[i].strip() not in Product_name[j] and group_names[item]=='Firmware binary posting':
                        add_to_alt_summary_content(inc,2,Product_name[j],'Blue')
                        
                    else:
                        add_to_alt_summary_content(inc,2,Product_name[j],False)
                        
                    add_to_alt_summary_content(inc,3,Date[j],False)
                    add_to_alt_summary_content(inc,4,Version[j],False)
                    add_to_alt_summary_content(inc,5,Os[j],False)
                    
                    if File_name[j]=='Not Found':
                        add_to_alt_summary_content(inc,6,File_name[j],'Red_Bold')
                    else:
                        add_to_alt_summary_content(inc,6,File_name[j],False)
                    
                    add_to_alt_summary_content(inc,7,Download_url[j],False)
                    add_to_alt_summary_content(inc,8,Description[j],False)
                    add_to_alt_summary_content(inc,9,Severity[j],False)
        
            if group_name_flag==True:
                inc+=1
                
                add_to_alt_summary_content(inc,0,Card_name[i],'Column0')
                add_to_alt_summary_content(inc,1,Input_part_numbers[i],'Column1')
                
                if condition_status_check==True:
                    add_to_alt_summary_content(inc,2,'Not Supported','Green_Bold')
                    condition_status_check=False
                elif group_names[item]=='Firmware binary posting':
                    add_to_alt_summary_content(inc,2,'No firmware posting for '+Input_part_numbers[i]+' found','Red_Bold')
                else:
                    add_to_alt_summary_content(inc,2,'No Products found','Red_Bold')

                
                add_to_alt_summary_content(inc,3,' ',False)
                add_to_alt_summary_content(inc,4,' ',False)
                add_to_alt_summary_content(inc,5,' ',False)
                add_to_alt_summary_content(inc,6,' ',False)
                add_to_alt_summary_content(inc,7,' ',False)
                add_to_alt_summary_content(inc,8,' ',False)
                add_to_alt_summary_content(inc,9,' ',False)
                

def add_to_input_sheet_content(row,column,value,format):
    global input_sheet_content
    input_sheet_content.append(row)
    input_sheet_content.append(column)
    input_sheet_content.append(value)
    input_sheet_content.append(format)
    
def insert_input_sheet():
    
    global summary_content
    global alt_summary_content
    global input_sheet_content
    
    for i in range(0,len(Input_part_numbers)):
        
        if i==0:                    # Making Header of the table as bold
            format = 'Bold'
        else:
            format = False
        
        add_to_input_sheet_content(i,0,Input_part_numbers[i],format)
        add_to_input_sheet_content(i,1,Card_name[i],format)
        add_to_input_sheet_content(i,2,Chipset[i],format)
        add_to_input_sheet_content(i,3,Type[i],format)
        add_to_input_sheet_content(i,4,WinOF_support[i],format)
        add_to_input_sheet_content(i,5,WinOF2_support[i],format)
        add_to_input_sheet_content(i,6,OFED4_support[i],format)
        add_to_input_sheet_content(i,7,OFED5_support[i],format)
        add_to_input_sheet_content(i,8,VM_support[i],format)
        add_to_input_sheet_content(i,9,MFT_support[i],format)
        add_to_input_sheet_content(i,10,Windows_fw_support[i],format)
        add_to_input_sheet_content(i,11,Linux_RoCE_support[i],format)
        add_to_input_sheet_content(i,12,FW_binary_support[i],format)
        add_to_input_sheet_content(i,13,FWPKG_support[i],format)
        
    
    summary_content.insert(0,input_sheet_content)               # Adding input sheet as the first sheet in both the summary excel fies.
    alt_summary_content.insert(0,input_sheet_content)


output_path                                                     =   get_output_path()
input_file , summary_output_file , alt_summary_output_file      =   create_output_files(output_path)
search_elem, group_names, short_group_names                     =   get_keywords()



Part_numbers        =   extract(input_file,0)               # All the part numbers from unique report
Product_name        =   extract(input_file,1)               
Date                =   extract(input_file,2)
Version             =   extract(input_file,3)
Os                  =   extract(input_file,4)
File_name           =   extract(input_file,5)
Download_url        =   extract(input_file,6)
Description         =   extract(input_file,7)
Severity            =   extract(input_file,8)

Input_part_numbers  =   extract(sys.argv[1],0)              # All the part numbers from Audit Input file
Card_name           =   extract(sys.argv[1],1)
Chipset             =   extract(sys.argv[1],2)
Type                =   extract(sys.argv[1],3)
WinOF_support       =   extract(sys.argv[1],4)
WinOF2_support      =   extract(sys.argv[1],5)
OFED4_support       =   extract(sys.argv[1],6)
OFED5_support       =   extract(sys.argv[1],7)
VM_support          =   extract(sys.argv[1],8)
MFT_support         =   extract(sys.argv[1],9)
Windows_fw_support  =   extract(sys.argv[1],10)
Linux_RoCE_support  =   extract(sys.argv[1],11)
FW_binary_support   =   extract(sys.argv[1],12)
FWPKG_support       =   extract(sys.argv[1],13)

summary_content     =   []
alt_summary_content =   []
input_sheet_content =   []
sheet_list1=[]
sheet_list2=[]

if __name__=='__main__':
    logger = get_logger()         # Create a logger for debug file                                          
    logger.debug("Fetching part number and keyword froms search file")      
    logger.debug("Summarizing into excel sheet with each part number as separate sheets")
    summary()           # Create a summary excel file
    logger.debug("Summarizing into excel sheet with each group as separate sheets")
    summary_alt()       # Create an alternate summary excel file
    logger.debug("Copying input file to the output file for reference")
    insert_input_sheet()    # Adding the input sheet at the start of the bpth summary files.
    
    obj1=ExcelUtility(0)    # Object for summary and alt summary excel file
    obj2=ExcelUtility(1) 
    
    
    sheet_list1.append('input')     # sheet_list1 contains the sheet names of the sumary excel file.
    sheet_list2.append('input')     # sheet_list2 contains the sheet names of the alternate summary excel file.
    
    for i in range (1,len(Input_part_numbers)):
        sheet_list1.append(Input_part_numbers[i])
    
    for i in range (1,len(short_group_names)):
        sheet_list2.append(short_group_names[i])

    

    obj1.write_to_excel_file(summary_output_file,sheet_list1,summary_content)   # Writing it into the both excel files with the help of excelutility class obect.
    obj2.write_to_excel_file(alt_summary_output_file,sheet_list2,alt_summary_content)
    
    logger.info("Summary file = "+str(summary_output_file))
    logger.info("Alternative summary file = "+str(alt_summary_output_file))
    
    logger.debug(str(summary_content))
    
    print("\n Output files are stored in the folder ' "+output_path+'\\Audit_'+sys.argv[2]+" '")