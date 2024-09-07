from tkinter import filedialog as fd
from pdf_handler import DataExtract
from xml2json import xml2json
from json2xml import json_to_xml 
from constants import *
import time

FILETYPES = (('xml files', '*.xml'), ('all files', '*.*'))
pdf_convert = DataExtract()
XML_DIR = '/home/landotech/Documents/GitHub/drawmate.me/data/xml_files/'


def get_user_input(prompt):
    # Receive user input and call the proper function. 
    num_templates = 0
    
    if prompt == 1:
        # Create JSON file from a XML upload. Must be in draw.io XML format.
        xml_filepath = fd.askopenfilename(initialdir='~/Documents', filetypes=FILETYPES)
        xml_obj = xml2json(xml_filepath)
        # Get name for new template. xml2json will place a timestamp and add the template to the database.
        template_name = input("Enter a name for the new template: ")
        xml_obj.write_json(f'{template_name}')
    elif prompt == 2:
        pdf_convert.convert_pdf(new_file_name='pdf_extract')
    elif prompt == 3:
        # Get the list of current templates and render it to the user.
        for i in view_templates():
            num_templates += 1
            print(f'\n[{num_templates}] {i}')
        choose_temp = int(input('\nPlease select a template to export: '))
        new_xml_file = str(input('\nPlease provide a name for your new draw.io diagram: '))
        # Render the draw.io XML file and write to disk.
        for template in range(len(export_json_templates())):
            if choose_temp - 1 == template:
                json_obj = json_to_xml(export_json_templates()[template], f'{XML_DIR}/{new_xml_file}.drawio.xml') 
        print('successfull export\n')
    elif prompt == 4:
        pass
    elif prompt == 5:
        for i in view_templates():
            print(f'\n{i}')
    elif prompt == 6:
        pass
    else:
        print("Please select an option 1-6")


should_continue = True

while should_continue:
    prompt = int(input(""
                       "\nWelcome to drawmate. Please select from the following options:\n\n"
                       "\t[1] Upload draw.io XML file and save as template\n"
                       "\t[2] Upload PDF\n"
                       "\t[3] Export template to draw.io\n"
                       "\t[4] Add/Delete Templates\n"
                       "\t[5] View current templates\n"
                       "\t[6] View Documentation\n"
                       "\t[7] Exit\n\n"))
    if prompt == 7:
        print("exiting....")
        time.sleep(1)
        print("Goodbye")
        should_continue == False
        break
    else:
        get_user_input(prompt)

