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
        self._init_left_frame()
        self._init_root_canvas()
        self._init_listbox()

        # Add menu bar
        self.menu_bar()
        
        # Init notebook for tabular functions 
        self.notebook1 = ttk.Notebook(self.root)
        self.notebook1_state = tk.BooleanVar(value=False)
        
        # Set configs for ttk widgets
        self.set_ttk_configs()
 
        # Call mainloop
        self.root.mainloop()

    def set_root_configs(self):
        """
        Set root configs, color_pallete, window_size, title etc...
        Defines the main ui components for the child elements.
        """
        # Define color_pallete
        self.root.tk_setPalette(
                    background=self.config.color_pallete.get('light_grey'),
                    foreground=self.config.color_pallete.get('white'),
                    highlightBackground=self.config.color_pallete.get('purple'),
                    highlightForeground=self.config.color_pallete.get('white'),
                    selectBackground=self.config.color_pallete.get('red'),
                    selectForeground=self.config.color_pallete.get('white'),
                    activeBackground=self.config.color_pallete.get('purple'),
                    activeForeground=self.config.color_pallete.get('black'),
                )

        # Set window size
        self.root.minsize(width=600, height=400)
        self.root.maxsize(height=400)

        # Set title
        self.root.title('drawmate.me')

    def set_ttk_configs(self):
        # Set style for ttk widgets
        self.ttk_style = ttk.Style(self.root)
        self.ttk_style.theme_use('alt')

        # Set style for notebook widget
        self.ttk_style.configure(
                    'TNotebook',
                    background=self.config.color_pallete.get('light_grey'),
                    foreground=self.config.color_pallete.get('white'),
                    font=self.config.font_regular,
                    padding=10,
                )

        self.ttk_style.map('TNotebook',
                           background=[('selected',
                                        self.config.color_pallete.get('red')),
                                        ],
                           foreground=[('selected',
                                        self.config.color_pallete.get('white')),
                                        ]
                           )

        self.ttk_style.configure('TNotebook.Tab',
                                 background=self.config.color_pallete.get('light_grey'),
                                 foreground=self.config.color_pallete.get('black'))

        # Set style for treeview widget
        self.ttk_style.configure(
                    'Treeview',
                    background=self.config.color_pallete.get('light_grey'),
                    foreground=self.config.color_pallete.get('white'),
                    font=self.config.font_regular,
                    )

        # Set mapping for treeview widget
        self.ttk_style.map('Treeview',
                           background=[('selected',
                                        self.config.color_pallete.get('red'))],
                           foreground=[('selected',
                                        self.config.color_pallete.get('white'))])
    
    def _init_root_canvas(self):
        self.root_canvas = tk.Canvas(master=self.root)
        self.root_canvas.pack(side='top', padx=10, pady=10)


    def _init_left_frame(self):
        # Add frame to left side of window 
        self.l_frame = tk.Frame(master=self.root)
        self.l_frame.pack(side='top', padx=10, pady=10)
        self.l_frame.config(relief='flat', borderwidth=1)

        # Add label to frame
        self.main_label = tk.Label(master=self.l_frame)
        self.main_label.config(text='drawmate', font=self.config.font_large)
        self.main_label.pack()

        # Init menu buttons for l_frame
        self.upload_button_xml()
        self.upload_button_pdf()
        self.export_button_json()
        self.view_templates_button()

    def _init_listbox(self):
        """
        Defines the listbox element and configures basic elements/commands.
        """
        # Instantiate/configure listbox for viewing templates
        self.listbox_submit_state = tk.BooleanVar(value=False)
        self.destroy_listbox_state = tk.BooleanVar(value=False)
        self.listbox_state = tk.BooleanVar(value=False)

        if self.listbox_state.get() == False:
            self.listbox = tk.Listbox(master=self.root_canvas)
            self.listbox_state.set(value=True)
            self.listbox.config(selectmode='single',
                                relief='flat',
                                borderwidth=2,
                                font=self.config.font_regular,
                                activestyle='none',
                                )
            self.listbox_label = tk.Label(master=self.root_canvas, text='JSON Templates:')
            self.listbox_label.config(font=self.config.font_bold)

        if self.listbox_submit_state.get() == False:
            # Create listbox submit button
            self.listbox_submit = tk.Button(master=self.root_canvas)
            self.listbox_submit_state.set(value=True)
            self.listbox_submit.configure(text='Generate Treeview',
                                          relief='flat',
                                          command=self.submit_listbox_button,
                                          font=self.config.font_regular)

        if self.destroy_listbox_state.get() == False: 
            # Create listbox exit button
            self.destroy_listbox = tk.Button(master=self.root_canvas)        
            self.destroy_listbox_state.set(value=True)
            self.destroy_listbox.config(text='Close',
                                        command=self.drestroy_listbox,
                                        relief='flat',
                                        font=self.config.font_regular)

        def on_up(event):
            # Get current selection and highlight by moving arrow key up
            current_selection = self.listbox.curselection()
            if current_selection:
                index = current_selection[0]
                if index > 0:
                    self.listbox.selection_clear(index)
                    self.listbox.selection_set(index - 1)
                    self.listbox.activate(index - 1)

        def on_down(event):
            # Get current selection and highlight by moving arrow key down
            current_selection = self.listbox.curselection()
            if current_selection:
                index = current_selection[0]
                if index < self.listbox.size() - 1:
                    self.listbox.selection_clear(index)
                    self.listbox.selection_set(index + 1)
                    self.listbox.activate(index + 1)           

        def on_enter(event):
            current_selection = self.listbox.curselection()
            json_data = self.on_listbox_select().get('json_data') 
            tab_name = self.on_listbox_select().get('tab_name')
            self.tree_view(json_data, tab_name)

        self.listbox.bind('<Up>', on_up)
        self.listbox.bind('<Down>', on_down)
        self.listbox.bind('<Return>', on_enter)

    def _init_tree(self, tab_frame):
        # Instantiate/configure treeview widget
        self.tree = ttk.Treeview(master=tab_frame)
        self.tree.configure(height=125)
        self.tree['column'] = ('diagram',)
        self.tree.column('diagram',
                    width=400,
                    minwidth=200,
                    stretch=tk.NO)
        self.tree.heading('#0',
                     text='drawio',
                     anchor=tk.W)
        self.tree.heading('diagram', text='values', anchor=tk.W)
        
        # Add button to close treeview 
        self._init_tree_close_button()

    def _init_tree_close_button(self):
        # Add button to close treeview 
        if not hasattr(self, 'tree_close_button'):
            self.tree_close_button = tk.Button(master=self.root_canvas, command=self.close_tree)
            self.tree_close_button.configure(text='Exit Treeview',
                                             relief='flat',
                                             borderwidth=2,
                                             font=self.config.font_regular)
            self.tree_close_button_state = tk.BooleanVar(value=True)
            self.tree_close_button.pack(side='bottom', padx=10, pady=10)

        if self.tree_close_button_state.get() == False:
            self.tree_close_button = tk.Button(master=self.root_canvas, command=self.close_tree)
            self.tree_close_button.configure(text='Exit Treeview',
                                             relief='flat',
                                             borderwidth=2,
                                             font=self.config.font_regular)
            self.tree_close_button_state = tk.BooleanVar(value=True)
            self.tree_close_button.pack(side='bottom', padx=10, pady=10)

    def drestroy_listbox(self):
            # Destroy listbox widget
            self.listbox.destroy()
            self.listbox_state.set(value=False)

            # Destroy listbox buttons/labels
            self.listbox_submit.destroy()
            self.listbox_submit_state.set(value=False)
            self.destroy_listbox.destroy()
            self.destroy_listbox_state.set(value=False)
            self.listbox_label.destroy()

    # Top Menu Bar
    def menu_bar(self):
        # Create menu bar
        menu_bar = tk.Menu(master=self.root)
        menu_bar.config(font=self.config.font_regular)
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
        button.pack(side='left', padx=10, pady=10, expand=True)
        button.config(text='Upload XML',
                      command=self.open_input_dialog_xml,
                      relief='flat',
                      borderwidth=2,
                      font=self.config.font_regular)

    def upload_button_pdf(self):
        # Button to upload pdf. File is passed to pdfhandler class to extract relevant data
        pdf_button = tk.Button(master=self.l_frame)
        pdf_button.pack(side='left', padx=10, pady=10, expand=True)
        pdf_button.config(text='Upload PDF',
                          command=self.open_input_dialog_pdf,
                          relief='flat',
                          borderwidth=2,
                          font=self.config.font_regular)
       
    def export_button_json(self):
        # Export json template to xml
        export_button = tk.Button(master=self.l_frame)
        export_button.pack(side='left', padx=10, pady=10, expand=True)
        export_button.config(text='Export JSON',
                             command=self.open_input_dialog_json,
                             relief='flat',
                             borderwidth=2,
                             font=self.config.font_regular)

    def view_templates_button(self):
        # Button to view json templates
        view_button = tk.Button(master=self.l_frame)
        view_button.pack(side='left', padx=10, pady=10, expand=True)
        view_button.config(text='View Templates',
                           command=self.view_templates,
                           relief='flat',
                           borderwidth=2,
                           font=self.config.font_regular)

    # Commands for buttons inside of left frame widget
    def view_templates(self):
        self._init_listbox()
        # Get a list of templates from the template directory and pass it to the listbox
        if os.path.isdir(self.JSON_DIR):
            self.listbox.delete(0, tk.END)
            for item in self.export_json_templates():
                strip_item = item.split('/')
                self.listbox.insert(tk.END, strip_item[-1])
        else:
            print("Invalid path")
        
        # Init listbox and scrollbars
        self.listbox_label.pack(side='top', padx=10, pady=10)
        self.listbox.pack(padx=10, pady=10, side='top')
        self.destroy_listbox.pack(padx=10, pady=10, side='bottom')
        self.listbox_submit.pack(side='bottom', padx=10, pady=10)
        self.listbox.config(width=50, height=20)
    
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
        # Check if notebook1 has been initialized 
        if self.notebook1_state.get() == False:
            self.notebook1 = ttk.Notebook(master=self.root_canvas)
            self.notebook1_state.set(value=True)

        tab_frame = ttk.Frame(master=self.notebook1)
        self.notebook1.add(tab_frame, text=tab_name)
       
        # Call tree function 
        self._init_tree(tab_frame)

        # Insert root node to tree
        root_node = self.tree.insert('', 'end', text='mxfile') 
            
        def create_tree(parent_node, data):
            for k, v in data.items():
                if isinstance(v, dict):
                    node_id = self.tree.insert(parent_node, 'end', text=k)
                    create_tree(node_id, v)
                else:
                    self.tree.insert(parent_node, 'end', text=k, values=(v,))

        # Recursive function call
        create_tree(root_node, json_data)

        # Pack notebook1, tree, and button to close tree
        self.notebook1.pack(side='bottom', padx=10, pady=10)
        self.tree.pack(side='top', padx=10, pady=10)

    def close_tree(self):
        # Destroy treeview widget
        self.tree.destroy()

        # Destroy notebook widget
        self.notebook1.destroy()

        # Update notebook state
        self.notebook1_state.set(value=False)

        # Destroy button to clean up canvas
        self.tree_close_button.destroy()
        self.tree_close_button_state.set(value=False)
        print('Treeview destroyed')

    def on_listbox_select(self):
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
                
                listbox_select = {'json_data': json_data, 'tab_name': tab_name}

                return listbox_select
                
    def submit_listbox_button(self):
        if not self.listbox.curselection():
            return
        else: 
            json_data = self.on_listbox_select().get('json_data')
            tab_name = self.on_listbox_select().get('tab_name')
            self.tree_view(json_data, tab_name)


if __name__ == "__main__":
    RootWindow()
