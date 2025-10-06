import os, glob, sys, time


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