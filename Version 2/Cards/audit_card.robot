*** Settings ***

Library    Python_files\\CreateExcelFile.py
Library    OperatingSystem
Library    String
Library    Process
Library    Selenium2Library  timeout=20  run_on_failure=Nothing

Library    Python_files\\fetch.py
Library    Collections
Library    python_files\\new_file.py


*** Variables ***

@{content}
${val}=  0
${search}=  not found
@{status1}  PASS  1
${flag}
${output_file}


*** Test Cases ***

Test main

    @{part_numbers}   extract    ${input_file}     0  # fetching all  the data from column 0 of input file and appending it to a list name conf_files

    FOR  ${part_number}  IN   @{part_numbers}
        continue for loop if  '${part_number}'=='Part Number' 
        set global variable  ${flag}  Bold
        Append to List  ${content}  0  0  Part Number  ${flag}
        Append to list  ${content}  0  1  Product name  ${flag}
        Append to list  ${content}  0  2  Date  ${flag}
        Append to list  ${content}  0  3  Version  ${flag}
        Append to list  ${content}  0  4  OS  ${flag}
        Append to list  ${content}  0  5  Download Page  ${flag}
        Append to list  ${content}  0  6  Description  ${flag}
        Append to list  ${content}  0  7  Severity  ${flag}
        set global variable  ${flag}  False
        run keyword and ignore error  Reach Product Page  ${part_number}
        ${total_count}  get text  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[4]/div[1]/div[5]/div[21]/ul[1]/li[1]/label[1]/div[1]/span[1]  # getting total conut of the product (from field besides All dates in the left column)
        log to console  ${part_number} ${total_count}
        ${condition}  run keyword and ignore error  Product loop  ${part_number}  ${total_count}
        run keyword if  '${condition}[0]'=='FAIL'  Test error entry  ${part_number} 
        close all browsers
    END

    ${out_file}=    get file    config.txt    encoding=UTF-8
    @{out_lines}=   split to lines  ${out_file}

    FOR    ${out_elem}  IN   @{out_lines}
        @{out_words}=	Split String	${out_elem}	    ${SPACE}
        run keyword if  '@{out_words}[0]'=='output_path='  set global variable  ${output_file}  @{out_words}[1]
    END

    log to console  ${content}
    create directory  ${output_file}\\Audit_${day}
    write to excel file1    ${output_file}\\Audit_${day}\\Audit_report_consolidated_${day}.xlsx    ${content}
    close all browsers
*** Keywords ***

Page loop   # depricated
    [Arguments]  ${part_number}  
    FOR  ${inc}  IN RANGE  3  10
        Product loop  ${part_number}
        ${status1}  run keyword and ignore error  click element  xpath://span[@class='coveo-pager-next-icon']             
        sleep  20
        ${status2}  run keyword if  '${status1}[0]'=='FAIL'  run keyword and ignore error  click element  xpath:/html[1]/body[1]/div[3]/div[2]/div[1]/div[3]/button[2]
        run keyword and ignore error  continue for loop if  '${status2}'=='None'
        sleep  2
        ${status1}  run keyword if  '${status2}[0]'=='PASS'  run keyword and ignore error  click element  xpath://span[@class='coveo-pager-next-icon'] 
        run keyword and ignore error  exit for loop if  '${status1}'=='None'
        run keyword and ignore error  exit for loop if  '${status1}[0]'=='FAIL'
    END


Product loop
    [Arguments]  ${part_number}  ${total_count}
    ${limit}=  Evaluate  ${total_count}+1  

    FOR  ${element}  IN RANGE  1  ${limit}
        ${prod_name}  run keyword and ignore error  get text  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[4]/div[2]/div[14]/div[1]/div[1]/div[${element}]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1] 
        continue for loop if  '${prod_name}[0]'=='FAIL'  
        ${date}  run keyword and ignore error  get text  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[4]/div[2]/div[14]/div[1]/div[1]/div[${element}]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]
        ${version}  run keyword and ignore error  get text  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[4]/div[2]/div[14]/div[1]/div[1]/div[${element}]/div[1]/div[1]/div[2]/div[1]/div[3]/div[1]
        run keyword and ignore error  click element  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[4]/div[2]/div[14]/div[1]/div[1]/div[${element}]/div[1]/div[1]/div[3]/div[1]/div[1]/span[1]    # more details field
        sleep  2
        ${download_page}  run keyword and ignore error  get text  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[4]/div[2]/div[14]/div[1]/div[1]/div[${element}]/div[1]/div[1]/div[3]/div[1]/div[2]/table[1]/tbody[1]/tr[1]/td[1]
        ${description}  run keyword and ignore error  get text  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[4]/div[2]/div[14]/div[1]/div[1]/div[${element}]/div[1]/div[1]/div[3]/div[1]/div[2]/table[1]/tbody[1]/tr[2]/td[1]
        ${severity}  run keyword and ignore error  get text  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[4]/div[2]/div[14]/div[1]/div[1]/div[${element}]/div[1]/div[1]/div[3]/div[1]/div[2]/table[1]/tbody[1]/tr[3]/td[1]
        ${os}  run keyword and ignore error  get text  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[4]/div[2]/div[14]/div[1]/div[1]/div[${element}]/div[1]/div[1]/div[3]/div[1]/div[2]/table[1]/tbody[1]/tr[4]/td[1]
        ${temp}=  Evaluate  ${val}+1  
        set global variable  ${val}  ${temp}
        run keyword if  '${prod_name}[0]'=='PASS'   Append to list  ${content}  ${val}    0    ${part_number}    ${flag}
        run keyword if  '${prod_name}[0]'=='PASS'   Append to list  ${content}  ${val}    1    ${prod_name}[1]  ${flag}
        run keyword if  '${date}[0]'=='PASS'  Append to list  ${content}  ${val}    2    ${date}[1]  ${flag}
        run keyword if  '${version}[0]'=='PASS'  Append to list  ${content}  ${val}    3    ${version}[1]  ${flag}
        run keyword if  '${os}[0]'=='PASS'  Append to list  ${content}  ${val}    4    ${os}[1]  ${flag}
        run keyword if  '${download_page}[0]'=='PASS'  Append to list  ${content}  ${val}    5    ${download_page}[1]  ${flag}  
        run keyword if  '${description}[0]'=='PASS'  Append to list  ${content}  ${val}    6    ${description}[1]  ${flag}
        run keyword if  '${severity}[0]'=='PASS'  Append to list  ${content}  ${val}    7    ${severity}[1]  ${flag}
    END


Reach Product Page
    [Arguments]  ${part_number}

    FOR  ${trial}  IN RANGE  0  5   # Number of times that the webpage needs to be relaunched before reporting it as a Failed test.
       ${status}  run keyword and return status  Test launch  ${part_number}    # status representing the state of the web page launch. (from search page to product list page)
       exit for loop if  ${status}==True
       close all browsers
    END

    run keyword if  ${status}==False  Test error entry  ${part_number}  # Report the loading error.
    
Test launch
    [Arguments]  ${part_number}

    open browser    https://support.hpe.com/hpesc/public/home  ff  # Home page URL.
    sleep  10   # Waiting for the elements to get loaded.
    input text  xpath:/html[1]/body[1]/div[1]/div[1]/div[4]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[3]/div[3]/div[1]/input[1]  ${part_number}  # Enering the part number in search field of home page.
    click element  xpath:/html[1]/body[1]/div[1]/div[1]/div[4]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[3]/a[1]/span[1]   # clicking search button
    wait until page contains  All dates  timeout=1 min  # 1 minute time window for elements to appear on the web page.
    run keyword and ignore error  click element  xpath://p[contains(text(),'Drivers and Software')]     # selecting Drivers and Softwares.
    sleep  5
    run keyword and ignore error  click element  xpath:/html[1]/body[1]/div[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[4]/div[2]/div[6]/div[2]/span[1]/span[1]  # Selecting the list view.
    sleep  5
    run keyword and ignore error  click element  xpath://a[contains(text(),'All')]  # Selecting all the prooducts to be displayed on to the page.
    sleep  5
    click element  xpath://span[@id='datesort']     # sorting date wise.
    sleep  10
    

Test error entry
    [Arguments]  ${part_number}

    ${temp}=  Evaluate  ${val}+1  
    set global variable  ${val}  ${temp}
    Append to list  ${content}  ${val}    0    ${part_number}    ${flag}
    Append to list  ${content}  ${val}    1    No Products Found  ${flag}
    Append to list  ${content}  ${val}    2    ${SPACE}  ${flag}
    Append to list  ${content}  ${val}    3    ${SPACE}  ${flag}
    Append to list  ${content}  ${val}    4    ${SPACE}  ${flag}
    Append to list  ${content}  ${val}    5    ${SPACE}  ${flag}
    Append to list  ${content}  ${val}    6    ${SPACE}  ${flag}
    Append to list  ${content}  ${val}    7    ${SPACE}  ${flag}
    