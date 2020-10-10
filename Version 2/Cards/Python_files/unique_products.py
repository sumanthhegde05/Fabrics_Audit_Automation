import new_file
import fetch
import xlsxwriter
import sys


class ExcelUtility(object):

    
    def group(self,lst, n):
        """
        group([0,3,4,10,2,3], 2) => [(0,3), (4,10), (2,3)]
        """
        return zip(*[lst[i::n] for i in range(n)])
    
    
    def write_to_excel_file(self,filename,content_list):
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()
        worksheet.set_column('A:A', 20)
        worksheet.set_column('B:B', 50)
        worksheet.set_column('C:D', 20)
        worksheet.set_column('E:E', 40)
        worksheet.set_column('F:G', 50)
        worksheet.set_column('H:H', 20)
        cell_format = workbook.add_format({'align':'top', 'border':1 , 'border_color':'black'})
        cell_format.set_text_wrap()
        bold = workbook.add_format({'bold': True , 'align':'top' , 'align':'center' , 'bg_color':'yellow' , 'font_size':14 , 'border':2 , 'border_color':'black'})
        bold.set_text_wrap()
        t=self.group(content_list,4)
        
        for item in t:
            
            if item[3]=='Bold':
                worksheet.write(int(item[0]), int(item[1]), item[2],bold)
            else:
                worksheet.write(int(item[0]), int(item[1]), item[2],cell_format)
                
        workbook.close()


def main():
    for i in range (0, len(Product)):
        
        if Product[i]=='Product name':
            value='Bold' 
            
        if Part[i]+Product[i]+Os[i] not in temp :
            temp.append(Part[i]+Product[i]+Os[i])
            content.append(inc)
            content.append(0)
            content.append(Part[i])
            content.append(value)
            content.append(inc)
            content.append(1)
            content.append(Product[i])
            content.append(value)
            content.append(inc)
            content.append(2)
            content.append(Date[i])
            content.append(value)
            content.append(inc)
            content.append(3)
            content.append(Version[i])
            content.append(value)
            content.append(inc)
            content.append(4)
            content.append(Os[i])
            content.append(value)
            content.append(inc)
            content.append(5)
            content.append(Download_page[i])
            content.append(value)
            content.append(inc)
            content.append(6)
            content.append(Description[i])
            content.append(value)
            content.append(inc)
            content.append(7)
            content.append(Severity[i])
            content.append(value)
            inc+=1
            value=False
        else:
            pass
        
        
output_file=sys.argv[2]+"\\Audit_"+sys.argv[3]+"\\Audit_report_unique_"+sys.argv[3]+".xlsx" 
new_file.make_excel_file(output_file)
input_file      =   sys.argv[1]

Part            =   fetch.extract(input_file,0)
Product         =   fetch.extract(input_file,1)
Date            =   fetch.extract(input_file,2)
Version         =   fetch.extract(input_file,3)
Download_page   =   fetch.extract(input_file,5)
Description     =   fetch.extract(input_file,6)
Severity        =   fetch.extract(input_file,7)
Os              =   fetch.extract(input_file,4)

temp            =   []
content         =   []
inc             =   0


if __name__=='__main__':
    main() 
    obj=ExcelUtility()
    obj.write_to_excel_file(output_file,content)