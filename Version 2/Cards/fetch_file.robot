*** Settings ***

Library    Python_files\\CreateExcelFile.py
Library    OperatingSystem
Library    String
Library    Process
Library    Selenium2Library  timeout=20  run_on_failure=Nothing
Library    CreateExcelFile.ExcelUtility
Library    Python_files\\fetch.py
Library    Collections
Library    Python_files\\new_file.py


***Variables***

${input_file}
@{content}
${flag}  False
${pass_file}


***Test Cases***

Test main
    ${out_file}=    get file    config.txt    encoding=UTF-8
    @{out_lines}=   split to lines  ${out_file}

    FOR     ${out_elem}  IN   @{out_lines}
         @{out_words}=	Split String	${out_elem}	    ${SPACE}
         run keyword if  '@{out_words}[0]'=='output_path='  set global variable  ${output_file}  @{out_words}[1]
    END

    set global variable  ${pass_file}   ${output_file}\\Audit_${day}\\Audit_report_consolidated_${day}.xlsx
    start process   python   Python_files\\unique_products.py  ${pass_file}  ${output_file}  ${day}
    sleep  10
    set global variable  ${input_file}   ${output_file}\\Audit_${day}\\Audit_report_unique_${day}.xlsx
    @{part}=    extract    ${input_file}     0
    @{product}=    extract    ${input_file}     1
    @{date}=    extract    ${input_file}     2
    @{version}=    extract    ${input_file}     3
    @{os}=    extract    ${input_file}     4
    @{download}=    extract    ${input_file}     5
    @{description}=    extract    ${input_file}     6
    @{severity}=    extract    ${input_file}     7
    ${size}  Get Length  ${download}
    open browser  https://www.google.com  ff
    set global variable  ${flag}  Bold
    Append to List  ${content}  0  0  Part Number  ${flag}
    Append to list  ${content}  0  1  Product name  ${flag}
    Append to list  ${content}  0  2  Date  ${flag}
    Append to list  ${content}  0  3  Version  ${flag}
    Append to list  ${content}  0  4  OS  ${flag}
    Append to list  ${content}  0  5  File Name  ${flag}
    Append to list  ${content}  0  6  Download Page  ${flag}
    Append to list  ${content}  0  7  Description  ${flag}
    Append to list  ${content}  0  8  Severity  ${flag}
    set global variable  ${flag}  False

    FOR  ${inc}  IN RANGE  1  ${size} 
        ${err}  run keyword and ignore error  Test Launch  ${inc}  ${download}
        ${file_name2}  run keyword if  '${err}[0]'=='PASS'  Test continue
        run keyword if  ${err}=='FAIL'  set test variable  ${file_name2}  ${space}
        Append to List  ${content}  ${inc}  0  ${part}[${inc}]  ${flag}
        Append to list  ${content}  ${inc}  1  ${product}[${inc}]  ${flag}
        Append to list  ${content}  ${inc}  2  ${date}[${inc}]  ${flag}
        Append to list  ${content}  ${inc}  3  ${version}[${inc}]  ${flag}
        Append to list  ${content}  ${inc}  4  ${os}[${inc}]  ${flag}
        Append to list  ${content}  ${inc}  5  ${file_name2}  ${flag}
        Append to list  ${content}  ${inc}  6  ${download}[${inc}]  ${flag}
        Append to list  ${content}  ${inc}  7  ${description}[${inc}]  ${flag}
        Append to list  ${content}  ${inc}  8  ${severity}[${inc}]  ${flag}
    END

    write to excel file2  ${output_file}\\Audit_${day}\\Audit_report_unique_${day}.xlsx  ${content}
    sleep  10
    

***Keywords***

Test Launch
    [Arguments]  ${inc}  ${download}

    FOR  ${val}  IN RANGE  0  5
        ${err}  run keyword and ignore error  go to  ${download}[${inc}]
        run keyword if  '${download}[${inc}]'==''  FAIL
        sleep  5
        ${stat}  run keyword and return status  Page should contain  File name
        exit for loop if  ${stat}==True
    END

Test continue
    ${condition}    ${file_name}=   run keyword and ignore error    get text        xpath:/html[1]/body[1]/div[1]/div[1]/div[3]/div[1]/div[1]/table[3]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[2]/td[1]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[4]/td[2]
    ${status}  ${file_name2}  run keyword if  '${condition}'=='FAIL'  run keyword and ignore error   get text     xpath:/html[1]/body[1]/div[1]/div[1]/div[3]/div[1]/div[1]/table[3]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[2]/td[1]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[5]/td[2]
    ${compsig_status}  run keyword and return status  should contain  ${file_name2}  .compsig
    ${status2}  ${file_name3}  run keyword if  ${compsig_status}==True  run keyword and ignore error  get text  xpath:/html[1]/body[1]/div[1]/div[1]/div[3]/div[1]/div[1]/table[3]/tbody[1]/tr[1]/td[1]/table[1]/tbody[1]/tr[2]/td[1]/div[1]/div[1]/div[1]/table[1]/tbody[1]/tr[6]/td[2]
    run keyword if  ${compsig_status}==True  set test variable  ${file_name2}   ${file_name3}  
    run keyword if  '${condition}'=='PASS'  set test variable   ${file_name2}   ${file_name}
    run keyword if  '${status}'=='FAIL'  set test variable  ${file_name2}  Not Found  
    [return]  ${file_name2}
