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

        # Initialize configs
        self.set_root_configs()
        self.set_ttk_configs()
        self.config = AppConfig()

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
        """
        Initialize root canvas and declare the scrollbar.
        """

        # Init root canvas
        self.root_canvas = tk.Canvas(master=self.root)
        self.root_canvas.pack(side='top', padx=10, pady=10)

        # Configure scroll bar for root canvas
        self.yscroll = tk.Scrollbar(master=self.root_canvas,
                                    orient='vertical',
                                    command=self.root_canvas.yview)

        self.root_canvas.configure(yscrollcommand=self.yscroll.set)

        # Bind Configure option to the update_scroll_region method.
        # Call the _update_scroll_region method as the command
        self.root_canvas.bind("<Configure>", _update_scroll_region)

    def _init_menu_frame(self):
        # Add frame to left side of window 
        self.menu_frame = tk.Frame(master=self.root)
        self.menu_frame.pack(side='top', padx=10, pady=10)
        self.menu_frame.config(relief='flat', borderwidth=1)

        # Add label to frame
        self.menu_label = tk.Label(master=self.menu_frame)
        self.menu_label.config(text='drawmate', font=self.config.font_large)
        self.menu_label.pack()

        # Init menu buttons for l_frame
        self.upload_button_xml()
        self.upload_button_pdf()
        self.export_button_json()
        self.view_templates_button()

    def _init_listbox(self):
        """
        Defines the listbox widget and configures basic elements/commands.
        """
        self.listbox_state = tk.BooleanVar(value=False)
        self.listbox_submit_state = tk.BooleanVar(value=False)
        self.destroy_listbox_state = tk.BooleanVar(value=False)
        # Ensure listbox_state is False, then repopulate the listbox 
        # and reset state value
        if self.listbox_state.get() == False:
            # Init listbox and set parent element
            self.listbox = tk.Listbox(master=self.root_canvas)
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
            self.destroy_listbox.config(text='Close Templates',
                                        command=self.drestroy_listbox,
                                        relief='flat',
                                        font=self.config.font_regular)

