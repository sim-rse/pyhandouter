import os, sys
import time

from practicals import * 
from pdfStuff import *

args = sys.argv
overwrite = False
sucessful = False
output = "combined_handout.pdf"
addTitles = True

if len(args)>1:
    if args[1] == "True" or "true":
        overwrite = True


while True:
    cls()
    if overwrite:
        print("[Debug] - Overwriting mode enabled!")
    if sucessful:
        print("Handout sucessfully created!\n")
        time.sleep(1)
    inp = input(f"""┌────────────────────────────────┐
│     ── Python handouter ──     │
└────────────────────────────────┘
Give it a pdf and it'll turn it into a handout
(relative or absolute paths are fine in all cases)
                
1. Treat one single file 
2. Use list of files
3. Treat all pdf's in this directory
4. Treat all pdf's from a given directory
5. Change directory
6. Change output file name
-  any other: quit
                
The current directory is: {os.getcwd()}


Please insert choice: """)
    sucessful = False
    cls()
    match inp:
        case "1":
            pdf = [input("Paste the name of your file here: ")]
            insert_handouts_from_list(pdf, overwrite)
            sucessful = True
        case "2":
            lst = input("Please paste your list of files (all the names separated by commas, no brackets): ")
            pdf_list = lst.split(",")
            insert_handouts_from_list(pdf_list, output, addTitles, overwrite)
            sucessful = True
        case "3":
            pdf_list = get_all_pdf()
            insert_handouts_from_list(pdf_list, output, addTitles, overwrite)
            sucessful = True
        case "4":
            original = os.getcwd()
            path = input(f"Current directory: {os.getcwd()}\n\nPlease enter the path of the folder: ")
            path = path.strip('\'"')
            os.chdir(path) 
            pdf_list = get_all_pdf()
            insert_handouts_from_list(pdf_list, output, addTitles, overwrite)
            sucessful = True
            os.chdir(original)
        case "5":
            new_dir = input(f"Current directory: {os.getcwd()}\n\nPlease insert new directory: ")
            try:
                os.chdir(new_dir)
            except:
                input(f"There was an error finding your directory: {new_dir}\nPress any key to continue...")
        case "6":
            output = input("Please enter the new file name: ")
            output +=".pdf"
        case _:
            break