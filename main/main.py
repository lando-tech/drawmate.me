from tkinter import filedialog as fd
from pdf_handler import DataExtract
from xml2json import xml2json
from json2xml import *
from constants import *

FILETYPES = (('xml files', '*.xml'), ('all files', '*.*'))
pdf_convert = DataExtract()


def get_user_input():
    
    should_continue = True 
    while should_continue:
        prompt = int(input(""
                           "\nWelcome to drawmate. Please select from the following options:\n\n"
                           "\t[1] Upload draw.io XML file and save as template\n"
                           "\t[2] Upload PDF\n"
                           "\t[3] Export template to draw.io\n"
                           "\t[4] Create New Template\n"
                           "\t[5] View current templates\n"
                           "\t[6] Exit\n\n"))

        if prompt == 1:
            xml_filepath = fd.askopenfilename(initialdir='~/Documents', filetypes=FILETYPES)
            xml_obj = xml2json(xml_filepath)
            template_name = input("Enter a name for the new template: ")
            xml_obj.write_json(f'{template_name}')
        elif prompt == 2:
            pdf_convert.convert_pdf(new_file_name='pdf_extract')
        elif prompt == 3:
            pass
        elif prompt == 4:
            pass
        elif prompt == 5:
            for i in view_templates():
                print(i)
        elif prompt == 6:
            print('exiting...')
            should_continue == False
            break
        else:
            print("Please select an option 1-5")
            break


get_user_input()

