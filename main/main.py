from tkinter import filedialog as fd

FILETYPES = (('xml files', '*.xml'), ('all files', '*.*'))


prompt = int(input(""
                   "\nWelcome to drawmate. Please select from the following options:\n\n"
                   "\t[1] Upload draw.io XML file and save as template\n"
                   "\t[2] Upload PDF and convert to draw.io\n"
                   "\t[2] Create a diagram from template\n"
                   "\t[3] Create New Template\n"
                   "\t[4] View current templates\n"
                   "\t[5] Exit\n"))

while True:
    if prompt == 1:
        fd.askopenfilename(initialdir='~/Documents', filetypes=FILETYPES)
    elif prompt == 2:
        fd.askopenfilename(initialdir='~/Documents', filetypes=(('pdf files', '*.pdf'), ('all files', '*.*')))
    elif prompt == 3:
        pass
    elif prompt == 4:
        pass
    elif prompt == 5:
        break
