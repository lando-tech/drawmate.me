# Simple cli prompt to run tests on each module and ensure proper functionality

from tkinter import filedialog as fd
from pdf_handler import DataExtract
from xml2json import xml2json
from json2xml import json2xml 
from pathfinder import PathFinder as pf
from db import MyDB
import time
import subprocess

path_finder = pf()
pdf_convert = DataExtract()
db_conn = MyDB(db_name="templates.db", table_name="templates")

def get_user_input(prompt):
    # Receive user input and call the proper function. 
  
    if prompt == 1:
        convert_xml()
    elif prompt == 2:
        pdf_convert.convert_pdf(new_file_name='pdf_extract')
    elif prompt == 3:
        export_as_xml()
        print('\nsuccessfull export\n')
    elif prompt == 4:
        specify_file_type()
    elif prompt == 5:
        pass
    elif prompt == 6:
        show_templates() 
    elif prompt == 7:
        pass
    else:
        print("Please select an option 1-8")


def choose_template():
  
    num_templates = 0
    # Get the list of current templates and render it to the user.
    for i in path_finder.view_templates():
        num_templates += 1
        print(f'\n[{num_templates}] {i}')
    chosen_temp = int(input('\nPlease select a template to export (Please type the number of the template): '))
   
    return chosen_temp 


def name_of_file():
    file_name = str(input('\nPlease provide a name for the file: '))
    return file_name


def export_as_xml():
    # Iterate through templates and choose template based on user input to export
    template_choice = choose_template()
    new_xml_file = name_of_file()
    for template in range(len(path_finder.export_json_templates())):
        if template_choice - 1 == template:
            json2xml(path_finder.export_json_templates()[template], f'{path_finder.get_xml_export_dir()}{new_xml_file}.drawio.xml') 
   


def convert_xml():
    # Create JSON file from a XML upload. Must be in draw.io XML format.
    xml_filepath = fd.askopenfilename(initialdir='~/Documents', filetypes=path_finder.get_filetypes())
    xml_obj = xml2json(xml_filepath)
    # Get name for new template. xml2json will place a timestamp and add the template to the database.
    template_name = input("Enter a name for the new template: ")
    xml_obj.write_json(f'{template_name}')
    db_conn.add_entry(i="test", o=template_name)


def specify_file_type():
    arg1_format = None
    arg2_outpath = None
    arg3_inpath = None

    to_upload = input("Would you like to upload a drawio file? If yes type (y) or type (view) to select from a template: ").lower()

    if to_upload == "y":
        arg3_inpath = fd.askopenfilename(initialdir='~/Documents', filetypes=path_finder.get_filetypes())
    elif to_upload == "view":
        export_as_xml()
        arg3_inpath = path_finder.get_xml_exports()[-1]

    export_type = int(input(""
                "\n\tChoose a filetype:\n"
                "\t[1] HTML\n"
                "\t[2] PDF\n"
                "\t[3] SVG\n"
                "\t[4] PNG\n"))
    if export_type == 1:
        arg1_format = "html"
        f_name = name_of_file()
        arg2_outpath = f"{path_finder.get_html_dir()}{f_name}drawio.html"
    elif export_type == 2:
        arg1_format = "pdf"
        f_name = name_of_file()
        arg2_outpath = f"{path_finder.get_pdf_dir()}{f_name}.pdf"
    elif export_type == 3:
        arg1_format = "svg"
        f_name = name_of_file()
        arg2_outpath = f"{path_finder.get_svg_dir()}{f_name}.svg"
    elif export_type == 4:
        arg1_format = "png"
        f_name = name_of_file()
        arg2_outpath = f"{path_finder.get_png_dir()}{f_name}.png"

      
    bash_script = path_finder.get_script_dir()
    drawio_cli = subprocess.run([bash_script, arg1_format, arg2_outpath, arg3_inpath], capture_output=True, text=True)
    print(f"\nstdout: {drawio_cli.stdout}\nstderr: {drawio_cli.stderr}\n")


def show_templates():
    num_templates = 0
    for i in path_finder.view_templates():
        num_templates += 1
        print(f'\n\t[{num_templates}] {i}')


should_continue = True

while should_continue:
    prompt = int(input(""
                       "\nWelcome to drawmate. Please select from the following options:\n\n"
                       "\t[1] Upload draw.io XML file and save as template\n"
                       "\t[2] Upload PDF\n"
                       "\t[3] Export template to drawio.xml (standard)\n"
                       "\t[4] Specify export file type\n"
                       "\t[5] Add/Delete Templates\n"
                       "\t[6] View current templates\n"
                       "\t[7] View Documentation\n"
                       "\t[8] Exit\n\n"))
    if prompt == 8:
        print("exiting....")
        time.sleep(1)
        print("Goodbye")
        break
    else:
        get_user_input(prompt)

