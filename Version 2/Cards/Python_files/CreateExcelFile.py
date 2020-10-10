import xlsxwriter


class ExcelUtility(object):
    
    
    def group(self,lst, n):
        """
        group([0,3,4,10,2,3], 2) => [(0,3), (4,10), (2,3)]
        """
        return zip(*[lst[i::n] for i in range(n)])
    
    
    def write_to_excel_file1(self,filename,content_list):
            workbook = xlsxwriter.Workbook(filename)    # create an excel file.
            worksheet = workbook.add_worksheet()    #create a working sheet
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
        
        
    def write_to_excel_file2(self,filename,content_list):
            workbook = xlsxwriter.Workbook(filename)
            worksheet = workbook.add_worksheet()
            worksheet.set_column('A:A', 20)
            worksheet.set_column('B:B', 50)
            worksheet.set_column('C:D', 20)
            worksheet.set_column('E:E', 40)
            worksheet.set_column('F:H', 50)
            worksheet.set_column('I:I', 20)
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
