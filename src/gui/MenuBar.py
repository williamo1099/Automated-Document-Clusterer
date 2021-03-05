
from retrieval.Document import Document
from gui.window.AboutWindow import AboutWindow
from gui.WarningPopup import WarningPopup

import os
import tkinter as tk
from tkinter import filedialog
import pickle
import webbrowser

class MenuBar:
    
    def __init__(self, gui, preprocessor_option, autorenaming_option):
        """
        The constructor for MenuBar class.

        Parameters
        ----------
        gui : gui
            The main gui.
        preprocessor_option : list
            blabla
        autorenaming_option : 

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
        file_menu.add_command(label='Update index', command=self.update_index)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.gui.get_window().destroy)
        
        # Initialize the option menu in menu bar.
        for preprocessor_item in preprocessor_option:
            preprocessor_item.set(True)
        option_menu = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label='Option', menu=option_menu)
        option_menu.add_checkbutton(label='Stop words removal', onvalue=1, offvalue=0, variable=preprocessor_option[0])
        option_menu.add_checkbutton(label='Stemming', onvalue=1, offvalue=0, variable=preprocessor_option[1])
        option_menu.add_checkbutton(label='Case folding', onvalue=1, offvalue=0, variable=preprocessor_option[2])
        option_menu.add_checkbutton(label='Normalization', onvalue=1, offvalue=0, variable=preprocessor_option[3])
        option_menu.add_separator()
        autorenaming_option.set(True)
        option_menu.add_checkbutton(label='Auto-renamed clusters', onvalue=1, offvalue=0, variable=autorenaming_option)
        
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
    
    def update_index(self):
        """
        The method to update an inverted index.

        Returns
        -------
        None

        """
        folder_path = self.gui.get_folder_path()
        try:
            # Retrieve all .txt files in folder.
            curr_doc_titles = []
            for root, directories, files in os.walk(folder_path):
                for file in files:
                    if '.txt' in file:
                        curr_doc_titles.append(file.replace('.txt', ''))
            
            # Retrieve all saved documents' title.
            doc_titles = [doc.get_title() for doc in self.gui.get_corpus()]
            
            # Compare two document lists.
            difference = list(set(curr_doc_titles) - set(doc_titles))
            
            # Check if there is a difference between two document lists.
            if len(difference) == 0: 
                popup = WarningPopup('Updating an index',
                                     'The index is currently up to date!')
                popup.show_popup()
            else:
                extended_corpus = []
                for i in range(0, len(difference)):
                    doc_id = 'doc_' + str(i + len(self.gui.get_corpus()))
                    doc_title = difference[i]
                    doc_content = open(folder_path + '\\' + difference[i] + '.txt', 'r', encoding='utf-8').read().replace('\n', '')
                    doc_i = Document(doc_id, doc_title, doc_content)
                    extended_corpus.append(doc_i)
                
                # Update the corpus and inverted index.
                self.gui.set_corpus(self.gui.get_corpus() + extended_corpus)
                self.gui.update_inverted_index(extended_corpus)
        except EnvironmentError:
            popup = WarningPopup('Updating an index',
                                 'The file path of the saved index does not exist!')
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
        self.about_window = AboutWindow(self.gui)
        self.about_window.start()