from pathfinder import PathFinder
from xml2json import xml2json
from json2xml import JsonUtils
from pdf_handler import DataExtract 
from config import AppConfig
import os
import json
import tkinter as tk 
from tkinter import filedialog as fd 
from tkinter import ttk


class RootWindow(PathFinder, JsonUtils, DataExtract):
    """
    Main class for the drawmate UI.
    Initializes a main window and makes calls to the backend modules
    for data processing.
    """

    def __init__(self) -> None:
        super().__init__()
        # Init root window
        self.root = tk.Tk()
        self.config = AppConfig()
        self.set_root_configs()
        
        # Initialize major UI components
        self._init_main_frame()
        self._init_left_frame()
        self._init_listbox()

        # Add menu bar
        self.menu_bar()
        
        # Init notebook for tabular functions 
        self.notebook1 = ttk.Notebook(self.root)
        
        # Set configs for ttk widgets
        self.set_ttk_configs()
 
        # Call mainloop
        self.root.mainloop()


    def _init_main_frame(self):
        # Configure main frame for top of app
        self.main_frame = tk.Frame(master=self.root)
        self.main_frame.grid(column=0, row=0, padx=20, pady=20)
        
        # Configure welcome banner/label 
        self.main_label = tk.Label(master=self.main_frame)
        self.main_label.config(text='drawmate', font='16')
        self.main_label.pack()

    def _init_left_frame(self):
        # Add frame to left side of window 
        self.l_frame = tk.Frame(master=self.root)
        self.l_frame.grid(column=0, row=1, padx=10, pady=10)
        self.l_frame.config(relief='ridge', borderwidth=2)
        # Init menu buttons for l_frame
        self.upload_button_xml()
        self.upload_button_pdf()
        self.export_button_json()
        self.view_templates_button()

    def _init_listbox(self):
        # Instantiate/configure listbox for viewing templates
        self.listbox = tk.Listbox(master=self.l_frame)
        self.listbox.config(selectmode='single')
        self.listbox.bind('<<ListboxSelect>>', self.on_listbox_select)
    
        # Create Scrollbars for listbox
        self.listbox_y_scrollbar = tk.Scrollbar(master=self.l_frame)
        self.listbox_y_scrollbar.config(orient='vertical', command=self.listbox.yview)
        self.listbox_x_scrollbar = tk.Scrollbar(master=self.l_frame)
        self.listbox_x_scrollbar.config(orient='horizontal', command=self.listbox.xview)

    def set_root_configs(self):
        self.root.tk_setPalette(
                    background=self.config.color_pallete.get('light_grey'),
                    foreground=self.config.color_pallete.get('white'),
                    highlightBackground=self.config.color_pallete.get('purple'),
                    highlightForeground=self.config.color_pallete.get('white'),
                    selectBackground=self.config.color_pallete.get('white'),
                    selectForeground=self.config.color_pallete.get('black'),
                    activeBackground=self.config.color_pallete.get('purple'),
                    activeForeground=self.config.color_pallete.get('black')
                )
        self.root.minsize(width=600, height=600)
        self.root.title('drawmate.me')

    def set_ttk_configs(self):
        self.ttk_style = ttk.Style(self.root)
        self.ttk_style.configure(
                    'TNotebook',
                    background=self.config.color_pallete.get('light_grey'),
                    foreground=self.config.color_pallete.get('white'),
                    padding=10,
                )
        self.ttk_style.configure(
                    'Treeview',
                    background=self.config.color_pallete.get('light_grey'),
                    foreground=self.config.color_pallete.get('white'),
                )
        self.ttk_style.map('Treeview',
                           background=[('selected',
                                        self.config.color_pallete.get('white'))],
                           foreground=[('selected',
                                        self.config.color_pallete.get('black'))])

    # Top Menu Bar
    def menu_bar(self):
        # Create menu bar
        menu_bar = tk.Menu(master=self.root)
        menu_bar.config(font='12')
        # Create filemenu
        filemenu = tk.Menu(master=menu_bar, tearoff=0)
        # Set commands for filemenu 
        filemenu.add_command(label='Upload', command=None)
        filemenu.add_command(label='Open', command=None)
        filemenu.add_command(label='Save', command=None)
        filemenu.add_command(label='Export', command=None)
        # Call root to init menubar
        menu_bar.add_cascade(label='File', menu=filemenu)
        self.root.config(menu=menu_bar)
    
    # Buttons for left frame widget
    def upload_button_xml(self):
        # Upload xml file to app and convert to json
        button = tk.Button(master=self.l_frame)
        button.pack(padx=10, pady=10, expand=True)
        button.config(text='Upload XML',
                      command=self.open_input_dialog_xml,
                      relief='ridge',
                      borderwidth=2)

    def upload_button_pdf(self):
        # Button to upload pdf. File is passed to pdfhandler class to extract relevant data
        pdf_button = tk.Button(master=self.l_frame)
        pdf_button.pack(padx=10, pady=10, expand=True)
        pdf_button.config(text='Upload PDF',
                          command=self.open_input_dialog_pdf,
                          relief='ridge',
                          borderwidth=2)
       
    def export_button_json(self):
        # Export json template to xml
        export_button = tk.Button(master=self.l_frame)
        export_button.pack(padx=10, pady=10, expand=True)
        export_button.config(text='Export JSON',
                             command=self.open_input_dialog_json,
                             relief='ridge',
                             borderwidth=2)

    def view_templates_button(self):
        # Button to view json templates
        view_button = tk.Button(master=self.l_frame)
        view_button.pack(padx=10, pady=10, expand=True)
        view_button.config(text='View Templates',
                             command=self.view_templates,
                             relief='ridge',
                             borderwidth=2)
    
    # Commands for buttons inside of left frame widget
    def view_templates(self):
        # Get a list of templates from the template directory and pass it to the listbox
        if os.path.isdir(self.JSON_DIR):
            self.listbox.delete(0, tk.END)
            for item in os.listdir(self.JSON_DIR):
                self.listbox.insert(tk.END, item)
        else:
            print("Invalid path")
        
        # Init listbox and scrollbars
        self.listbox.pack(padx=10, pady=10, side=tk.LEFT, fill=tk.BOTH)
        self.listbox.config(xscrollcommand=self.listbox_x_scrollbar.set,
                            yscrollcommand=self.listbox_y_scrollbar.set)
        self.listbox_x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.listbox_y_scrollbar.pack(side=tk.LEFT, fill=tk.Y)

    def upload_xml(self, file_path, temp_name):
        # Function call for upload button
        self.xml_util = xml2json(file_path)
        self.xml_util.write_json(temp_name=temp_name)

    def export_json(self, file_path, xml_path):
        # Function call for export button
        self.json2xml(file_path, xml_path)

    def open_input_dialog_xml(self):
        # Open filedialog and save filepath into variable
        file_path = fd.askopenfilename(initialdir='~/Downloads',
                                       filetypes=self.FILETYPES[0])
        if not file_path:
            return
        # Open dialog to provide template name
        dialog = tk.Toplevel()
        dialog.title('Entry')
        dialog.minsize(50, 20)
        tk.Label(dialog, text='Enter name for file:').pack(padx=10, pady=10)
        
        entry_1 = tk.Entry(dialog)
        entry_1.pack(padx=10, pady=10)
        
        def submit():
            # Submit the template name and filepath to the upload function for processing
            temp_name = entry_1.get()
            dialog.destroy()
            self.upload_xml(file_path=file_path, temp_name=temp_name)

        # Submit button
        tk.Button(dialog, text='Submit', command=submit).pack()

    def open_input_dialog_json(self):
        # Open filedialog and save filepath into variable
        project_dir = self.JSON_DIR
        file_path = fd.askopenfilename(initialdir=f'{project_dir}', filetypes=self.FILETYPES[1])
        if not file_path:
            return
        # Open dialog to provide template name
        dialog = tk.Toplevel()
        dialog.title('Entry')
        dialog.minsize(50, 20)
        tk.Label(dialog, text='Enter name for file:').pack(padx=10, pady=10)
        
        entry_1 = tk.Entry(dialog)
        entry_1.pack(padx=10, pady=10)
        
        def submit():
            # Submit the template name and filepath to the upload function for processing
            file_name = entry_1.get()
            xml_f_path = f'{self.XML_EXPORT_DIR}/{file_name}.drawio.xml'
            dialog.destroy()
            self.export_json(file_path, xml_f_path)

        # Submit button
        tk.Button(dialog, text='Submit', command=submit).pack()

    def open_input_dialog_pdf(self):
        # Open dialog to provide template name
        dialog = tk.Toplevel()
        dialog.title('Entry')
        dialog.minsize(50, 20)
        tk.Label(dialog, text='Enter name for file:').pack(padx=10, pady=10)
        
        entry_1 = tk.Entry(dialog)
        entry_1.pack(padx=10, pady=10)
        
        def submit():
            # Submit the template name and filepath to the upload function for processing
            file_name = entry_1.get()
            dialog.destroy()
            self.convert_pdf(new_file_name=file_name)
        # Submit button
        tk.Button(dialog, text='Submit', command=submit).pack()
    
    # Initialize treeview widget
    def tree_view(self, json_data, tab_name):
        # Add tab for notebook 
        tab_frame = tk.Frame(master=self.notebook1)
        self.notebook1.add(tab_frame, text=tab_name)

        # Instantiate/configure treeview widget
        self.tree = ttk.Treeview(master=tab_frame)
        self.tree['column'] = ('diagram',)
        self.tree.column('diagram',
                    width=400,
                    minwidth=200,
                    stretch=tk.NO)
        self.tree.heading('#0',
                     text='drawio',
                     anchor=tk.W)
        self.tree.heading('diagram', text='Diagram', anchor=tk.W)

        # Insert root node to tree
        root_node = self.tree.insert('', 'end', text='mxfile') 

        def close_tree():
            self.notebook1.destroy()
            tree_close_button.destroy()

        def create_tree(parent_node, data):
            for k, v in data.items():
                if isinstance(v, dict):
                    node_id = self.tree.insert(parent_node, 'end', text=k)
                    create_tree(node_id, v)
                else:
                    self.tree.insert(parent_node, 'end', text=k, values=(v,))

        create_tree(root_node, json_data)
        self.notebook1.grid(column=0, row=2, padx=10, pady=10)

        # Add button to close treeview 
        tree_close_button = tk.Button(master=self.l_frame, command=close_tree)

        # Configure options for treeview
        tree_close_button.configure(text='Exit Treeview',
                                    relief='ridge',
                                    borderwidth=2)

        tree_close_button.pack(padx=10, pady=10)
        self.tree.grid(column=1, row=1, padx=20, pady=20)

    def on_listbox_select(self, event):
        """
        Function to grab the current listbox selection and pass
        it to the tree_view function
        """
        selected_index = self.listbox.curselection()
        if not selected_index:
            return
        selected_template = self.listbox.get(selected_index)
        template_path = os.path.join(self.JSON_DIR, selected_template)

        def get_tab_name():
            list_template = selected_template.split()
            return list_template[0]

        if os.path.isfile(template_path):
            with open(template_path, 'r') as file:
                json_data = json.load(file) 
                tab_name = get_tab_name()
                self.tree_view(json_data, tab_name)


if __name__ == "__main__":
    RootWindow()
