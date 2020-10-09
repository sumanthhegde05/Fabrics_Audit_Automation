import sys,os
from datetime import datetime
import time
from optparse import OptionParser,OptionGroup
import logging

help_message = "\n -i, --input [input_file_path] \n"

def get_date():
    now = datetime.now()
    #print("now =", now)
    date = now.strftime("%m-%d-%Y"+'_'+"%H-%M-%S")
    print("date and time =", date)
    return date	

def main():
    date = get_date()
    os.system('cmd /c "robot -v input_file:"'+sys.argv[2]+'" -v day:"'+date+'" audit_card.robot"')
    time.sleep(10)
    print("Fetching file name...")
    os.system('cmd /c "robot -v day:"'+date+'" fetch_file.robot"')
    time.sleep(10)
    print("Summarizing...")
    os.system('cmd /c "py Python_files\\summary.py "'+sys.argv[2]+'" "'+date)        
    print("END")
        
def add_options (parser):
    """
    Method that defines the options(prameters) for the script.
    """
    parser.add_option("-h","--help",  help = help_message , action="store_true",default = False)
    parser.add_option("-i","--input", help = "input file path", default = None)

    
def initialize():
    add_options(parser)                                                                 
    (options, args) = parser.parse_args()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler("debug.log",mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter('%(levelname)s : %(message)s'))
    """console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(message)s'))"""
    logger.addHandler(file_handler)
    #logger.addHandler(console_handler)
    return options , logger

parser = OptionParser(add_help_option=False)
options , logger = initialize()

if __name__=='__main__':
    if options.help:
        print(help_message)
        sys.exit()
    elif options.input != None:
        main()
    else:
        print("-h, --help for help message")
        
#10-08-2020_12-33-11
