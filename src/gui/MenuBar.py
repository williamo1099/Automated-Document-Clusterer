
from gui.AboutWindow import AboutWindow
from gui.WarningPopup import WarningPopup

import tkinter as tk
from tkinter import filedialog
import pickle
import webbrowser

class MenuBar:
    
    def __init__(self, gui):
        """
        The constructor for MenuBar class.

        Parameters
        ----------
        gui : gui
            The main gui.

        Returns
        -------
        None.

        """
        self.gui = gui
        
        # Initialize the menu bar in window.
        menu = tk.Menu(master=self.gui.get_window())
        self.gui.get_window().config(menu=menu)
        
        # Inititalize the file menu in menu bar.
        file_menu = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='New file', command=self.new_window)
        file_menu.add_command(label='Save index', command=self.save_index)
        file_menu.add_command(label='Load index', command=self.load_index)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.gui.get_window().destroy)
        
        # Initialize the help menu in menu bar.
        help_menu = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label='Help', menu=help_menu)
        help_menu.add_command(label='Documentation', command=self.documentation)
        help_menu.add_separator()
        help_menu.add_command(label='About', command=self.about)
        
    def new_window(self):
        """
        The method to reset the window.

        Returns
        -------
        None.

        """
        self.gui.restart()
        
    def save_index(self):
        """
        The method to save an inverted index as a pickle file.

        Returns
        -------
        None.

        """
        index_path = filedialog.asksaveasfilename(defaultextension='.pickle', filetypes=(('pickle file', '*.pickle'),))
        
        # Check whether an index is built or not.
        if self.gui.get_inverted_index() is not None:
            
            # Store metadata (probably useful in the future).
            metadata = {}
            metadata['folder_path'] = self.gui.get_folder_path()
            metadata['corpus'] = self.gui.get_corpus()
            
            # Store index and metadata.
            data = {}
            data['index'] = self.gui.get_inverted_index()
            data['metadata'] = metadata
            with open(index_path, 'wb') as handle:
                pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            popup = WarningPopup('Saving an index',
                                 'There is no index to be saved!')
            popup.show_popup()
            
    def load_index(self):
        """
        The method to load a saved inverted index.

        Returns
        -------
        None.

        """
        index_path = filedialog.askopenfilename()
        try:
            with open(index_path, 'rb') as handle:
                data = pickle.load(handle)

                # Load the inverted index.
                self.gui.set_inverted_index(data['index'])
                
                # Load the metadata.
                metadata = data['metadata']
                self.gui.set_folder_path(metadata['folder_path'])
                self.gui.set_corpus(metadata['corpus'])
                
                # Set the cluster status to True, indicating clustering process is ready to do.
                self.gui.set_cluster_status(True)
                popup = WarningPopup('Loading an index',
                                 'An index is successfully loaded!')
                popup.show_popup()
        except EnvironmentError:
            popup = WarningPopup('Loading an index',
                                 'There is no index to be loaded!')
            popup.show_popup()
    
    def documentation(self):
        """
        The method to show documentation on GitHub.
        This feature is currently not available.

        Returns
        -------
        None.

        """
        webbrowser.open('https://github.com/williamo1099/Skripsi-2020')
        
    def about(self):
        """
        The method to show an overview of the application.

        Returns
        -------
        None.

        """
        about_window = AboutWindow(self.gui)