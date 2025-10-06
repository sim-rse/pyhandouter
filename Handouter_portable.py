from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

import os, sys, time, re, glob

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def loading_bar(x, toolbar_width = 20):
    for i in x:
        # setup toolbar

        sys.stdout.write(i)
        sys.stdout.flush()
        sys.stdout.write("[%s]" % (" " * toolbar_width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['

        for i in range(toolbar_width):
            time.sleep(0.01) # do real work here
            # update the bar
            sys.stdout.write("■")
            sys.stdout.flush()

        sys.stdout.write("]\n") # this ends the progress bar
    
def get_all_pdf(path = "."):
    path = path + "\\"
    pdf_list= glob.glob(f"{path}*.pdf")
    return pdf_list

def uniquify(path):         #if name already exists it makes a new file with numbers
    filename, extension = os.path.splitext(path)
    counter = 0

    while os.path.exists(path):
        print(f"found file called {path}")
        path = filename + "(" + str(counter) + ")" + extension
        counter += 1
    if counter == 0:
        path = filename + extension
    return path

def natural_key(s): #used for sorting the file names correctly (the "human way") because else python would just look at the first numbers it encounters: you'd get something like ["file_1", "file_10", "file_2"] 
    # Splits the string into text and number chunks
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def create_blank_slide_with_lines(width, height):
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(width, height))
    c.setFont("Helvetica", 10)

    num_lines = 6
    line_height = 85
    margin = 40
    margin_top = 85
    c.setLineWidth(2)

    for i in range(num_lines):
        c.line(margin, height - (i * line_height) - margin_top, width - margin, height - (i * line_height) - margin_top)

    c.save()
    packet.seek(0)
    return packet

def create_title_slide(width, height, title):
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(width, height))
    c.setFont("Helvetica-Bold", 24)
    text_width = c.stringWidth(title, "Helvetica-Bold", 24)
    c.drawString((width - text_width) / 2, height / 2, title)
    c.save()
    packet.seek(0)
    return packet

def insert_handouts_from_list(input_pdf_paths:list, output_path, addTitles = False, overwrite = False):
        writer = PdfWriter()

        for input_pdf_path in input_pdf_paths:

            if os.path.splitext(os.path.basename(output_path))[0] in input_pdf_path:    #if there's a file with combined_handout in it, it's likely an older combined handout. To avoid mistakes and large files i'ts ignored
                print(f"Found and ignored a file contaning \"{output_path}\": {input_pdf_path}")
                continue

            reader = PdfReader(input_pdf_path)
            first_page = reader.pages[0]
            width = float(first_page.mediabox[2])
            height = float(first_page.mediabox[3])

            #adds first page
            writer.add_page(first_page)

            if addTitles:
                # Add title slide with filename
                title = os.path.basename(input_pdf_path)
                title_slide = create_title_slide(width, height, title)
                title_slide_pdf = PdfReader(title_slide)
                writer.add_page(title_slide_pdf.pages[0])

            # Create blank slide template
            blank_slide = create_blank_slide_with_lines(width, height)

            for page in reader.pages[1:]:
                writer.add_page(page)
                blank_slide_pdf = PdfReader(blank_slide)
                writer.add_page(blank_slide_pdf.pages[0])

        try:
            with open(output_path,"wb") as output:
                writer.write(output)
        except FileNotFoundError:
            print(f"[ERROR] The file called {output} was not found. Please check if the file exists and if you're working in the right directory.S")


#-----------main script-----------

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