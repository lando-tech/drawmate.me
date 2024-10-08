from datetime import datetime
from tkinter import filedialog as fd
from utils.pathfinder import PathFinder as pf
import pandas as pd
import pathlib
import pymupdf
import re
import os
import time


FILETYPES = (('pdf files', '*.pdf'), ('all files', '*.*'))
path_finder = pf()



class DataExtract:

    def __init__(self):
        # Initialize list of file names stored in the data directory
        self.file_names = os.listdir(path_finder.get_text_dir())
        # Initialize current date variable to add the date to the file name
        self.current_date = datetime.today()

    def convert_csv(self, **kwargs):
        """
        Returns a dataframe from the products database using the pandas library. This facilitates the
        comparison against the user provided data in order to build the wire-diagram.
        :param kwargs:
        :return:
        """
        csv_file = kwargs['path_to_file']
        app_data = pd.read_csv(f'{csv_file}', index_col=0)
        return app_data

    def convert_html(self):
        pass

    def convert_pdf(self, **kwargs):
        """
        Converts the pdf file selected by the user into a txt file. It scrapes all text
        out of the file and writes the file to disk with a timestamp identifier. File name
        is designated as 'extract-timestamp.txt'. It then returns the file path and file size to be
        used in the status/progress bar in gui.py.
        :param kwargs: str (filename)
        :return:
        """
        path_to_pdf = fd.askopenfile(initialdir="~/", filetypes=FILETYPES)
        new_file = kwargs['new_file_name']
        with pymupdf.open(path_to_pdf) as doc:
            text = chr(12).join([page.get_text() for page in doc])
            pathlib.Path(
                f"{path_finder.TXT_DIR}extracted_text/{new_file}-{datetime.today()}" + ".txt").write_bytes(text.encode())
            while not pathlib.Path(new_file):
                try:
                    file_path = pathlib.Path(f"{new_file}")
                    file_size = os.path.getsize(f"{file_path}")
                finally:
                    return file_size, file_path
            else:
                time.sleep(1)
                pass

    def extract_data(self, **kwargs):
        """
        Extracts the data from the newly created txt file and uses the re.findall method to find patterns
        in the text. The patterns will be specified using **kwargs. After the patterns are identified, the
        data will then be appended to a new file (name specified using **kwargs). Utilizing this method the
        user will be able to append as many pattern searches as needed to the same file, or create a new file
        to use at a later time.
        :param kwargs:
        :return:
        """
        path_to_file = kwargs['file_path']
        pattern_1 = kwargs['pattern1']
        pattern_2 = kwargs['pattern2']
        new_file = kwargs['name_of_new_file']

        with open(f"{path_to_file}", "r", encoding="UTF-8") as new_data:
            text_in_data = str(new_data.readlines())
            part_nums = re.findall(f"{pattern_1}", text_in_data)
            extra_part_nums = re.findall(f"{pattern_2}", text_in_data)
        # This block parses through the data and writes the part numbers to a new file for later analysis.
        with open(f"{path_finder.TXT_DIR}formatted_extract/{new_file}", "a", encoding="UTF=8") as new_file:

            for part in part_nums:
                new_file.write(f"{part},\n")
            for extra in extra_part_nums:
                new_file.write(f"{extra},\n")

    def generate_objects(self, **kwargs):

        path_to_file = kwargs['file_path']
        app_data = self.convert_csv(path_to_file=f'{path_finder.CSV_DIR}product_data.csv')
        new_list = []
        with open(f'{path_to_file}', 'r') as doc:
            user_data = doc.readlines()
            # TODO Refactor this section to create a dictionary with the proper key value pairs
            for index, row in app_data.iterrows():
                for i in range(len(user_data)):
                    if user_data[i].strip() in row['part_num'] or user_data[i].strip() in row['model']:
                        new_list.append({f'{row['model']}': (user_data[i].strip(), row['description'])})
            
            return new_list
        # trimmed_list = []
        # num_match1 = 0
        # num_match2 = 0
        # num_match3 = 0
        # num_match4 = 0
        #
        # pattern_1 = kwargs['pattern1']
        # pattern_2 = kwargs['pattern2']
        # pattern_3 = kwargs['pattern3']
        # pattern_4 = kwargs['pattern4']
        #
        # for i in range(len(new_list)):
        #     match1 = re.findall(f"{pattern_1}", new_list[i])
        #     match2 = re.findall(f"{pattern_2}", new_list[i])
        #     match3 = re.findall(f"{pattern_3}", new_list[i])
        #     match4 = re.findall(f"{pattern_4}", new_list[i])
        #
        #     if match1:
        #         num_match1 += 1
        #         trimmed_list.append(f"{match1[i % len(match1)]}-{num_match1}")
        #     elif match2:
        #         num_match2 += 1
        #         trimmed_list.append(f"{match2[i % len(match2)]}-{num_match2}")
        #     elif match3:
        #         num_match3 += 1
        #         trimmed_list.append(f"{match3[i % len(match3)]}-{num_match3}")
        #     elif match4:
        #         num_match4 += 1
        #         trimmed_list.append(f"{match4[i % len(match4)]}-{num_match4}")
        #     else:
        #         continue
        #
        # return trimmed_list
