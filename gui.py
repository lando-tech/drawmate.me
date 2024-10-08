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

        # Set configs
        self.config = AppConfig()
        self.set_root_configs()
        self.set_ttk_configs()       

        # Initialize major UI components
        self._init_menu_bar()
        self._init_menu_frame()
        self._init_canvas_1()
        self._init_canvas_2()
        self._init_listbox()
        
        # Init notebook for tabular functions 
        self.notebook1 = ttk.Notebook(self.root)
        self.notebook1_state = tk.BooleanVar(value=False)

        # Declare listbox and listbox button's state values
        self.listbox_submit_state = tk.BooleanVar(value=False)
        self.listbox_destroy_state = tk.BooleanVar(value=False)
        self.listbox_state = tk.BooleanVar(value=False)

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
    
    def _init_menu_bar(self):
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
    
    def _init_canvas_1(self):
        """
        Initialize root canvas and declare the scrollbar.
        """

        # Init root canvas
        self.canvas_1 = tk.Canvas(master=self.root)
        self.canvas_1.pack(side='left', padx=10, pady=10)

        # Configure scroll bar for root canvas
        self.yscroll = tk.Scrollbar(master=self.canvas_1,
                                    orient='vertical',
                                    command=self.canvas_1.yview)

        self.canvas_1.configure(yscrollcommand=self.yscroll.set)

        # Bind Configure option to the update_scroll_region method.
        # Call the _update_scroll_region method as the command
        self.canvas_1.bind("<Configure>", self._update_scroll_region_root_canvas)
        
    def _update_scroll_region_root_canvas(self, e):
        """
        Update root_canvas dimensions to dynamically provide a mouse
        as the right size.
        """
        self.canvas_1.configure(scrollregion=self.canvas_1.bbox('all'))

    def _init_canvas_2(self):
        self.canvas_2 = tk.Canvas(master=self.root)
        self.canvas_2.pack(side='left', padx=10, pady=10)
            
    def _init_menu_frame(self):
        # Add frame to left side of window 
        self.menu_frame = tk.Frame(master=self.root)
        self.menu_frame.pack(side='top', padx=10, pady=10)
        self.menu_frame.config(relief='flat', borderwidth=1)

        # Add label to frame
        self.main_label = tk.Label(master=self.menu_frame)
        self.main_label.config(text='drawmate', font=self.config.font_large)
        self.main_label.pack()

        # Init menu buttons for l_frame
        self.upload_xml_button()
        self.upload_pdf_button()
        self.export_json_button()
        self.view_templates_button()

    def upload_xml_button(self):
        # Upload xml file to app and convert to json
        xml_button = tk.Button(master=self.menu_frame)
        xml_button.pack(side='left', padx=10, pady=10, expand=True)
        xml_button.config(text='Upload XML',
                      command=self.open_input_dialog_xml,
                      relief='flat',
                      borderwidth=2,
                      font=self.config.font_regular)

    def upload_xml(self, file_path, temp_name):
        # Function call for upload button
        self.xml_util = xml2json(file_path)
        self.xml_util.write_json(temp_name=temp_name)    
        
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

    def upload_pdf_button(self):
        # Button to upload pdf. File is passed to pdfhandler class to extract relevant data
        pdf_button = tk.Button(master=self.menu_frame)
        pdf_button.pack(side='left', padx=10, pady=10, expand=True)
        pdf_button.config(text='Upload PDF',
                          command=self.open_input_dialog_pdf,
                          relief='flat',
                          borderwidth=2,
                          font=self.config.font_regular)

    def open_input_dialog_pdf(self):
        """
        Calls the pdf conversion method from the DataExtract class.
        This method writes a txt file with the scrapped text from 
        the file operations. See pdf_handler.py docs for more info.
        """
        # Open dialog to provide template name
        dialog = tk.Toplevel()

        # Set title
        dialog.title('Entry')

        # Set dimensions
        dialog.minsize(50, 20)

        # Set label for dialog
        tk.Label(dialog, text='Enter name for file:').pack(padx=10, pady=10)
        
        # Set entry to retrieve user input
        entry_1 = tk.Entry(dialog)

        # Pack entry to canvas
        entry_1.pack(padx=10, pady=10)
        
        def submit():
            """
            Nested function used to submit the filepath/name of new file.
            """

            # Submit the template name and filepath to the upload function for processing
            file_name = entry_1.get()
            # Destroy dialog once input is retrieved
            dialog.destroy()
            # Call pdf conversion method
            self.convert_pdf(new_file_name=file_name)

        # Submit button for user entry 
        tk.Button(dialog, text='Submit', command=submit).pack()      

    def export_json_button(self):
        # Export json template to xml
        export_button = tk.Button(master=self.menu_frame)
        export_button.pack(side='left', padx=10, pady=10, expand=True)
        export_button.config(text='Export JSON',
                             command=self.open_input_dialog_json,
                             relief='flat',
                             borderwidth=2,
                             font=self.config.font_regular)

    def export_json(self, file_path, xml_path):
        # Function call for export button
        self.json2xml(file_path, xml_path)    

    def open_input_dialog_json(self):
        """
        Opens a filedialog in the JSON directory and retrieve user entry 
        to name the new file. 
        """
        # Open filedialog and save filepath into variable
        project_dir = self.JSON_DIR
        file_path = fd.askopenfilename(initialdir=f'{project_dir}', filetypes=self.FILETYPES[1])

        # Ensure filepath exists
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

    def view_templates_button(self):
        # Button to view json templates
        view_button = tk.Button(master=self.menu_frame)
        view_button.pack(side='left', padx=10, pady=10, expand=True)
        view_button.config(text='View Templates',
                           command=self.view_templates,
                           relief='flat',
                           borderwidth=2,
                           font=self.config.font_regular)

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
        self.yscroll.pack(side='right', fill='y')
        self.destroy_listbox.pack(padx=10, pady=10, side='top')
        self.listbox_submit.pack(side='top', padx=10, pady=10)
        self.listbox.config(width=40, height=20)    

    def _init_listbox(self):
        """
        Defines the listbox widget and configures basic elements/commands.
        """
        self.listbox_state = tk.BooleanVar(value=False)
        self.listbox_submit_state = tk.BooleanVar(value=False)
        self.listbox_destroy_state = tk.BooleanVar(value=False)

        # Ensure listbox_state is False, then repopulate the listbox 
        # and reset state value
        if self.listbox_state.get() == False:
            # Init listbox and set parent element
            self.listbox = tk.Listbox(master=self.canvas_1)
            # Reset listbox state
            self.listbox_state.set(value=True)
            # Set config options 
            self.listbox.config(selectmode='single',
                                relief='flat',
                                borderwidth=2,
                                font=self.config.font_regular,
                                activestyle='none',
                                height=20,
                                width=40,
                                )

            # Declare label for listebox
            self.listbox_label = tk.Label(master=self.canvas_1, text='JSON Templates:')
            self.listbox_label.config(font=self.config.font_bold)

        if self.listbox_submit_state.get() == False:
            # Create listbox submit button
            self.listbox_submit = tk.Button(master=self.canvas_1)
            self.listbox_submit_state.set(value=True)
            self.listbox_submit.configure(text='Generate Treeview',
                                          relief='flat',
                                          command=self.submit_listbox_button,
                                          font=self.config.font_regular)

        if self.listbox_destroy_state.get() == False: 
            # Create listbox exit button
            self.destroy_listbox = tk.Button(master=self.canvas_1)        
            self.listbox_destroy_state.set(value=True)
            self.destroy_listbox.config(text='Close Templates',
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

    def on_listbox_select(self):
        """
        Function to grab the current listbox selection and pass
        it to the tree_view function
        """

        # Current index of selection
        selected_index = self.listbox.curselection()

        # Check if index is selected, if false return None 
        # to avoid error
        if not selected_index:
            return

        # Get current selection
        selected_template = self.listbox.get(selected_index)

        # Join the json directory with the selected template 
        # in order to generate a correct file path
        template_path = os.path.join(self.JSON_DIR, selected_template)

        # Get the name of the tab based on template name list
        def get_tab_name():
            list_template = selected_template.split()
            return list_template[0]
        
        # Check if filepath exists
        if os.path.isfile(template_path):
            with open(template_path, 'r') as file:
                json_data = json.load(file) 
                tab_name = get_tab_name()
                
                listbox_select = {'json_data': json_data, 'tab_name': tab_name}

                return listbox_select
                
        else:
            print('Incorrect file path')    

    def submit_listbox_button(self):
        """
        Function behind the submit_listbox_button.
        This button is called once the button is pressed,
        or the return key is pressed.
        """

        # Check to ensure current selection is active
        if not self.listbox.curselection():
            return
        else: 
            json_data = self.on_listbox_select().get('json_data')
            tab_name = self.on_listbox_select().get('tab_name')
            self.tree_view(json_data, tab_name)    
    
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

    def _init_tree(self, tab_frame):
        """
        Function call to Instantiate treeview widget.
        """

        # Create treeview widget
        self.tree = ttk.Treeview(master=tab_frame)

        # Configure height of widget
        self.tree.configure(height=200)

        # Declare column name and dimensions
        self.tree['column'] = ('diagram',)
        self.tree.column('diagram',
                    width=400,
                    minwidth=200,
                    stretch=tk.NO)

        # Set treevieew heading
        self.tree.heading('#0',
                     text='drawio',
                     anchor=tk.W)
        self.tree.heading('diagram', text='values', anchor=tk.W)
        
        # Add button to close treeview 
        self._init_tree_close_button()

    def _init_tree_close_button(self):
        # Add button to close treeview 
        if not hasattr(self, 'tree_close_button'):
            self.tree_close_button = tk.Button(master=self.canvas_1, command=self.close_tree)
            self.tree_close_button.configure(text='Exit Treeview',
                                             relief='flat',
                                             borderwidth=2,
                                             font=self.config.font_regular)
            self.tree_close_button_state = tk.BooleanVar(value=True)
            self.tree_close_button.pack(side='bottom', padx=10, pady=10)

        if self.tree_close_button_state.get() == False:
            self.tree_close_button = tk.Button(master=self.canvas_1, command=self.close_tree)
            self.tree_close_button.configure(text='Exit Treeview',
                                             relief='flat',
                                             borderwidth=2,
                                             font=self.config.font_regular)
            self.tree_close_button_state = tk.BooleanVar(value=True)
            self.tree_close_button.pack(side='bottom', padx=10, pady=10)

    def tree_view(self, json_data, tab_name):
        """
        Uses the ttk.treeview widget to display a tree view 
        of the selected JSON template.
        """
        # Check if notebook1 has been initialized 
        if self.notebook1_state.get() == False:
            self.notebook1 = ttk.Notebook(master=self.canvas_2)
            self.notebook1_state.set(value=True)
        
        # Set tab frame for notebook widget
        tab_frame = ttk.Frame(master=self.notebook1)

        # Add tab to notebook
        self.notebook1.add(tab_frame, text=tab_name)
       
        # Call tree function 
        self._init_tree(tab_frame)

        # Insert root node to tree
        root_node = self.tree.insert('', 'end', text='mxfile') 

        # Recursively iterate through nodes 
        def create_tree(parent_node, data):
            for k, v in data.items():
                if isinstance(v, dict):
                    node_id = self.tree.insert(parent_node, 'end', text=k)
                    create_tree(node_id, v)
                else:
                    self.tree.insert(parent_node, 'end', text=k, values=(v,))

        # Recursive function call
        create_tree(root_node, json_data)

        # Pack notebook1(parent of tree) and tree
        self.notebook1.pack(side='bottom', padx=10, pady=10)
        self.tree.pack(side='top', padx=10, pady=10)

    def close_tree(self):
        """
        Closes treeview and destroys associated widgets 
        to clear the screen.
        """

        # Destroy treeview widget
        self.tree.destroy()

        # Destroy notebook widget
        self.notebook1.destroy()

        # Destroy scrollbar (parent is root_canvas)
        self.yscroll.destroy()

        # Update notebook state (state is used to redraw based on boolean value)
        self.notebook1_state.set(value=False)

        # Destroy button to clean up canvas
        self.tree_close_button.destroy()

        # Update button state
        self.tree_close_button_state.set(value=False)
        print('Treeview destroyed')


if __name__ == "__main__":
    RootWindow()
