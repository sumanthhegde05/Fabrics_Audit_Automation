import sys,os
from datetime import datetime
import time

now = datetime.now()
print("now =", now)
date = now.strftime("%m-%d-%Y"+'_'+"%H-%M-%S")
print("date and time =", date)	

if len(sys.argv)>1:
    if sys.argv[1]=='-help':
        print("Format:  py <scrpit to run>.py -input <input file path>")
    elif sys.argv[1]=='-input' and sys.argv[2]!='':
        os.system('cmd /c "robot -v input_file:"'+sys.argv[2]+'" -v day:"'+date+'" audit_new.robot"')
        time.sleep(10)
        os.system('cmd /c "robot -v day:"'+date+'" fetch_file.robot"')
        time.sleep(10)
        os.system('cmd /c "py Python_files\\summary.py "'+sys.argv[2]+'" "'+date)        
    else:
        print("Enter -help for input format")       
else:
    print("Enter -help for input format")
        
