*** Settings ***
Library    Python_files\\CreateExcelFileSwitch.py
Library    OperatingSystem
Library    String
Library    Process
Library    Selenium2Library  timeout=20  run_on_failure=Nothing
Library    CreateExcelFileSwitch.ExcelUtility
Library    Python_files\\fetch.py
Library    Collections
Library    python_files\\new_file.py

*** Variables ***
@{content}
${val}=  0
${search}=  not found
@{status1}  PASS  1
${flag}
${day}
${output_file}
${input_file}
*** Test Cases ***
Test main
    set global variable  ${day}  test
    set global variable  ${input_file}  input_switch.xlsx
    log to console  ${day}
    @{part_number}   extract    ${input_file}     0
    @{market_name}  extract   ${input_file}  1
    ${size}=  Get Length  ${part_number}
    log to console  total:${size}
    :For     ${elem}  IN RANGE   ${size}
    \   continue for loop if  '${part_number}[${elem}]'=='Part Number'
    \   log to console  ${part_number}[${elem}]
    \   set global variable  ${flag}  Bold
    \   Append to List  ${content}  0  0  Part Number  ${flag}
    \   Append to list  ${content}  0  1  Marketing Name  ${flag}
    \   Append to list  ${content}  0  2  Product name  ${flag}
    \   Append to list  ${content}  0  3  Date  ${flag}
    \   Append to list  ${content}  0  4  Version  ${flag}
    \   Append to list  ${content}  0  5  OS  ${flag}
    \   Append to list  ${content}  0  6  Download Page  ${flag}
    \   Append to list  ${content}  0  7  Description  ${flag}
    \   Append to list  ${content}  0  8  Severity  ${flag}
    \   set global variable  ${flag}  False
    \   make excel file  output.xlsx
    \   launch  ${part_number}[${elem}]
    \   Page loop  ${part_number}[${elem}]  ${market_name}[${elem}] 
    \   close all browsers
#    \   ${temp}=  Evaluate  ${val}+1  
#    \   set global variable  ${val}  ${temp}
    ${out_file}=    get file    config.txt    encoding=UTF-8
    @{out_lines}=   split to lines  ${out_file}
    :For     ${out_elem}  IN   @{out_lines}
    \    @{out_words}=	Split String	${out_elem}	    ${SPACE}
    \    run keyword if  '@{out_words}[0]'=='output_path='  set global variable  ${output_file}  @{out_words}[1]
    log to console  ${output_file}
    create directory  ${output_file}\\Audit_${day}
    write to excel file1    ${output_file}\\Audit_${day}\\Audit_report_consolidated_${day}.xlsx    ${content}

*** Keywords ***
Page loop
    [Arguments]  ${part_value}  ${market_value}  
    :For  ${inc}  IN RANGE  3  10
    \    log to console  page:${inc}
    \    log to console  ${status1}[0]
#    \    log to console  $decision_${decision}
    \    run keyword and ignore error  Product loop usual  ${inc}  ${part_value}  ${market_value}
#    \    run keyword if  '${decision}'=='PASS'  Product loop advanced  ${inc}  ${part_value}  ${market_value}
    \    ${status1}  run keyword and ignore error  click element  xpath://span[@class='coveo-pager-next-icon']             
    \    sleep  20
    \    log to console  ${status1}
    \    ${status2}  run keyword if  '${status1}[0]'=='FAIL'  run keyword and ignore error  click element  xpath:/html[1]/body[1]/div[3]/div[2]/div[1]/div[3]/button[2]
    \    log to console  ${status2}
    \    run keyword and ignore error  continue for loop if  '${status2}'=='None'
    \    sleep  2
    \    ${status1}  run keyword if  '${status2}[0]'=='PASS'  run keyword and ignore error  click element  xpath://span[@class='coveo-pager-next-icon'] 
    \    log to console  ${status1}
    \    run keyword and ignore error  exit for loop if  '${status1}'=='None'
    \    run keyword and ignore error  exit for loop if  '${status1}[0]'=='FAIL'

Product loop advanced
    [Arguments]  ${inc}  ${part_value}  ${market_value}
    :For  ${element}  IN RANGE  1  101
    \    log to console  product:${val}
    \    ${prod_name}  run keyword and ignore error  get text  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[4]/div[3]/div[5]/div[10]/div[1]/div[${element}]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]
    \    continue for loop if  '${prod_name}[0]'=='FAIL'     
    \    ${date}  run keyword and ignore error  get text  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[4]/div[3]/div[5]/div[10]/div[1]/div[${element}]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]
    \    ${version}  run keyword and ignore error  get text  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[4]/div[3]/div[5]/div[10]/div[1]/div[${element}]/div[1]/div[1]/div[2]/div[1]/div[3]/div[1]
    \    run keyword and ignore error  click element  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[4]/div[3]/div[5]/div[10]/div[1]/div[${element}]/div[1]/div[1]/div[3]/div[1]/div[1]/span[1]
    \    sleep  2
    \    ${download_page}  run keyword and ignore error  get text  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[4]/div[3]/div[5]/div[10]/div[1]/div[${element}]/div[1]/div[1]/div[3]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[1]
    \    ${description}  run keyword and ignore error  get text  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[4]/div[3]/div[5]/div[10]/div[1]/div[${element}]/div[1]/div[1]/div[3]/div[1]/div[2]/table[1]/tbody[1]/tr[2]/td[1]
    \    ${severity}  run keyword and ignore error  get text  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[4]/div[3]/div[5]/div[10]/div[1]/div[${element}]/div[1]/div[1]/div[3]/div[1]/div[2]/table[1]/tbody[1]/tr[3]/td[1]
    \    ${os}  run keyword and ignore error  get text  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[4]/div[3]/div[5]/div[10]/div[1]/div[${element}]/div[1]/div[1]/div[3]/div[1]/div[2]/table[1]/tbody[1]/tr[4]/td[1]
    \    ${temp}=  Evaluate  ${val}+1  
    \    set global variable  ${val}  ${temp}
    \    run keyword if  '${prod_name}[0]'=='PASS'   Append to list  ${content}  ${val}    0    ${part_value}   ${flag}
    \    run keyword if  '${prod_name}[0]'=='PASS'   Append to list  ${content}  ${val}    1    ${market_value}  ${flag}
    \    run keyword if  '${prod_name}[0]'=='PASS'   Append to list  ${content}  ${val}    2    ${prod_name}[1]  ${flag}
    \    run keyword if  '${date}[0]'=='PASS'  Append to list  ${content}  ${val}    3    ${date}[1]  ${flag}
    \    run keyword if  '${version}[0]'=='PASS'  Append to list  ${content}  ${val}    4    ${version}[1]  ${flag}
    \    run keyword if  '${os}[0]'=='PASS'  Append to list  ${content}  ${val}    5    ${os}[1]  ${flag}
    \    run keyword if  '${download_page}[0]'=='PASS'  Append to list  ${content}  ${val}    6    ${download_page}[1]  ${flag}
    \    run keyword if  '${description}[0]'=='PASS'  Append to list  ${content}  ${val}    7    ${description}[1]  ${flag}
    \    run keyword if  '${severity}[0]'=='PASS'  Append to list  ${content}  ${val}    8    ${severity}[1]  ${flag}

    #log to console  ${content}
Product loop usual
    [Arguments]  ${inc}  ${part_value}  ${market_value}
    :For  ${element}  IN RANGE  1  101
    \    log to console  product:${val}
    \    ${prod_name}  run keyword and ignore error  get text  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[4]/div[2]/div[14]/div[1]/div[1]/div[${element}]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]
    \    continue for loop if  '${prod_name}[0]'=='FAIL'  
    \    ${date}  run keyword and ignore error  get text  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[4]/div[2]/div[14]/div[1]/div[1]/div[${element}]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]
    \    ${version}  run keyword and ignore error  get text  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[4]/div[2]/div[14]/div[1]/div[1]/div[${element}]/div[1]/div[1]/div[2]/div[1]/div[3]/div[1]
    \    run keyword and ignore error  click element  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[4]/div[2]/div[14]/div[1]/div[1]/div[${element}]/div[1]/div[1]/div[3]/div[1]/div[1]/span[1]
    \    sleep  2
    \    ${download_page}  run keyword and ignore error  get text  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[4]/div[2]/div[14]/div[1]/div[1]/div[${element}]/div[1]/div[1]/div[3]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[1]
    \    ${description}  run keyword and ignore error  get text  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[4]/div[2]/div[14]/div[1]/div[1]/div[${element}]/div[1]/div[1]/div[3]/div[1]/div[2]/table[1]/tbody[1]/tr[2]/td[1]
    \    ${severity}  run keyword and ignore error  get text  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[4]/div[2]/div[14]/div[1]/div[1]/div[${element}]/div[1]/div[1]/div[3]/div[1]/div[2]/table[1]/tbody[1]/tr[3]/td[1]
    \    ${os}  run keyword and ignore error  get text  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[4]/div[2]/div[14]/div[1]/div[1]/div[${element}]/div[1]/div[1]/div[3]/div[1]/div[2]/table[1]/tbody[1]/tr[4]/td[1]
    \    ${temp}=  Evaluate  ${val}+1  
    \    set global variable  ${val}  ${temp}
    \    run keyword if  '${prod_name}[0]'=='PASS'   Append to list  ${content}  ${val}    0    ${part_value}   ${flag}
    \    run keyword if  '${prod_name}[0]'=='PASS'   Append to list  ${content}  ${val}    1    ${market_value}  ${flag}
    \    run keyword if  '${prod_name}[0]'=='PASS'   Append to list  ${content}  ${val}    2    ${prod_name}[1]  ${flag}
    \    run keyword if  '${date}[0]'=='PASS'  Append to list  ${content}  ${val}    3    ${date}[1]  ${flag}
    \    run keyword if  '${version}[0]'=='PASS'  Append to list  ${content}  ${val}    4    ${version}[1]  ${flag}
    \    run keyword if  '${os}[0]'=='PASS'  Append to list  ${content}  ${val}    5    ${os}[1]  ${flag}
    \    run keyword if  '${download_page}[0]'=='PASS'  Append to list  ${content}  ${val}    6    ${download_page}[1]  ${flag}
    \    run keyword if  '${description}[0]'=='PASS'  Append to list  ${content}  ${val}    7    ${description}[1]  ${flag}
    \    run keyword if  '${severity}[0]'=='PASS'  Append to list  ${content}  ${val}    8    ${severity}[1]  ${flag}

launch
    [Arguments]  ${part_value}
    :For  ${trial}  IN RANGE  0  2
    \   ${status}  ${decision}  run keyword and ignore error  Test try  ${part_value}
    \   log to console  launch_status:${status}
    \   exit for loop if  '${status}'=='PASS'
    \   close all browsers
    run keyword if  '${status}'=='FAIL'  Test error entry  ${part_value}

Test try
    [Arguments]  ${part_value}
    open browser    https://support.hpe.com/hpesc/public/home  ff
    maximize browser window
    sleep  10
    run keyword and ignore error  input text  xpath:/html[1]/body[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[3]/div[3]/div[1]/input[1]  ${part_value}             
    run keyword and ignore error  click element  xpath:/html[1]/body[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[3]/a[1]/span[1]
    run keyword and ignore error  wait until page contains  All dates  timeout=1 min
    #run keyword and ignore error  click element  xpath://p[contains(text(),'Products')]
    #sleep  5
    #${decision}  run keyword and ignore error  click element  xpath://a[contains(text(),'InfiniBand Switches')]
    #log to console  decision_${decision}[0]
    #sleep  5
    #run keyword if  '${decision}[0]'=='PASS'  input text  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[3]/div[1]/div[2]/div[1]/div[1]/input[1]  ${part_value}
    #run keyword if  '${decision}[0]'=='PASS'  click element  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[3]/div[1]/div[2]/a[1]/span[1]  
    #run keyword if  '${decision}[0]'=='FAIL'  go back
    #sleep  10
    ${success}  run keyword and ignore error  page should contain  All date 
    log to console  success_${success} 
    run keyword if  '${success}[0]'=='FAIL'  FAIL
    run keyword and ignore error  click element  xpath://p[contains(text(),'Drivers and Software')]
    sleep  5
    run keyword and ignore error  click element  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[4]/div[2]/div[6]/div[2]/span[1]/span[1]
    #run keyword if  '${decision}[0]'=='PASS'    run keyword and ignore error  click element  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[4]/div[3]/div[5]/div[3]/div[2]/span[1]/span[1]
    sleep  5
    run keyword and ignore error  click element  xpath://a[@class='coveo-results-per-page-list-item-text'][contains(text(),'100')]
    sleep  5
    run keyword and ignore error  click element  xpath://span[@id='datesort']
    sleep  10
    #${total_count}  run keyword if  '${decision}[0]'=='PASS'  run keyword and ignore error  get text  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[4]/div[2]/div[24]/ul[1]/li[1]/label[1]/div[1]/span[1]
    ${total_count}  run keyword and ignore error  get text  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[4]/div[1]/div[5]/div[28]/ul[1]/li[1]/label[1]/div[1]/span[1]
    log to console  ${total_count}

Test error entry
    [Arguments]  ${part_number}
    ${temp}=  Evaluate  ${val}+1  
    set global variable  ${val}  ${temp}
    Append to list  ${content}  ${val}    0    ${part_number}  ${flag}
    Append to list  ${content}  ${val}    1    No Products Found  ${flag}
    Append to list  ${content}  ${val}    2    ${SPACE}  ${flag}
    Append to list  ${content}  ${val}    3    ${SPACE}  ${flag}
    Append to list  ${content}  ${val}    4    ${SPACE}  ${flag}
    Append to list  ${content}  ${val}    5    ${SPACE}  ${flag}
    Append to list  ${content}  ${val}    6    ${SPACE}  ${flag}
    Append to list  ${content}  ${val}    7    ${SPACE}  ${flag}
    log to console  ${content}