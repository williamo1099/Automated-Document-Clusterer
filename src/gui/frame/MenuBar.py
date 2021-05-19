
from retrieval.Document import Document
from gui.window.AboutWindow import AboutWindow
from gui.window.WarningPopup import WarningPopup

import os
import threading
import pickle
import webbrowser
import tkinter as tk
from tkinter import filedialog

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
        self.__gui = gui
        
        # Initialize the menu bar in window.
        menu = tk.Menu(master=self.__gui.window)
        self.__gui.window.config(menu=menu)
        
        # Inititalize the file menu in menu bar.
        file_menu = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='New file', command=self.__new_window)
        file_menu.add_command(label='Save index', command=self.__save_index)
        file_menu.add_command(label='Load index', command=self.__load_index)
        file_menu.add_separator()
        file_menu.add_command(label='Update index', command=self.__update_index)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.__gui.window.destroy)
        
        # Initialize the option menu in menu bar.
        for preprocessor_item in self.__gui.preprocessor_option:
            preprocessor_item.set(True)
        option_menu = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label='Option', menu=option_menu)
        option_menu.add_checkbutton(label='Stop words removal', onvalue=1, offvalue=0, variable=self.__gui.preprocessor_option[0])
        option_menu.add_checkbutton(label='Stemming', onvalue=1, offvalue=0, variable=self.__gui.preprocessor_option[1])
        option_menu.add_checkbutton(label='Case folding', onvalue=1, offvalue=0, variable=self.__gui.preprocessor_option[2])
        option_menu.add_checkbutton(label='Normalization', onvalue=1, offvalue=0, variable=self.__gui.preprocessor_option[3])
        option_menu.add_separator()
        self.__gui.autorenaming_option.set(True)
        option_menu.add_checkbutton(label='Auto-renamed clusters', onvalue=1, offvalue=0, variable=self.__gui.autorenaming_option)
        
        # Initialize the help menu in menu bar.
        help_menu = tk.Menu(menu, tearoff=False)
        menu.add_cascade(label='Help', menu=help_menu)
        help_menu.add_command(label='Documentation', command=self.__documentation)
        help_menu.add_separator()
        help_menu.add_command(label='About', command=self.__about)
        
    def __new_window(self):
        """
        The method to reset the window.

        Returns
        -------
        None.

        """
        self.__gui._restart()
        
    def __save_index(self):
        """
        The method to save an inverted index as a pickle file.

        Returns
        -------
        None.

        """
        # Check whether an index is built or not.
        if self.__gui.inverted_index is not None:
            index_path = filedialog.asksaveasfilename(defaultextension='.pickle', filetypes=(('pickle file', '*.pickle'),))
            
            # Store metadata.
            metadata = {}
            metadata['folder_path'] = self.__gui.folder_path
            metadata['corpus'] = self.__gui.corpus
            
            # Store preprocessor options.
            preprocessor_option = []
            preprocessor_option.append(self.__gui.preprocessor_option[0].get())
            preprocessor_option.append(self.__gui.preprocessor_option[1].get())
            preprocessor_option.append(self.__gui.preprocessor_option[2].get())
            preprocessor_option.append(self.__gui.preprocessor_option[3].get())
            metadata['preprocessor_option'] = preprocessor_option
            
            # Store index and metadata.
            data = {}
            data['index'] = self.__gui.inverted_index
            data['metadata'] = metadata
            with open(index_path, 'wb') as handle:
                pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            popup = WarningPopup(self.__gui, 'Saving an index',
                                 'There is no index to be saved!')
            popup._start()
            
    def __load_index(self):
        """
        The method to load a saved inverted index.

        Returns
        -------
        None.

        """
        index_path = filedialog.askopenfilename(filetypes=(('pickle file', '*.pickle'),))
        try:
            with open(index_path, 'rb') as handle:
                data = pickle.load(handle)

                # Check whether the file loaded is the correct index file.
                if isinstance(data, dict) and 'index' in data and 'metadata' in data and 'folder_path' in data['metadata'] and 'corpus' in data['metadata']:
                    # Load the inverted index.
                    self.__gui.inverted_index = data['index']
                    
                    # Load the metadata.
                    metadata = data['metadata']
                    self.__gui.folder_path = metadata['folder_path']
                    self.__gui.corpus = metadata['corpus']
                    self.__gui.preprocessor_option = metadata['preprocessor_option']
                    
                    # Set the cluster status to True, indicating clustering process is ready to do.
                    self.__gui.cluster_status = True
                    popup = WarningPopup(self.__gui, 'Loading an index',
                                     'An index is successfully loaded!')
                    popup._start()
                else:
                    popup = WarningPopup(self.__gui, 'Loading an index',
                                     'File loaded does not match!')
                    popup._start()
        except EnvironmentError:
            popup = WarningPopup(self.__gui, 'Loading an index',
                                 'There is no index to be loaded!')
            popup._start()
    
    def __update_index(self):
        """
        The method to update an inverted index.

        Returns
        -------
        None

        """
        # Check whether an index is built or not.
        if self.__gui.inverted_index is not None:
            folder_path = self.__gui.folder_path
            try:
                # Retrieve all .txt files in folder.
                curr_doc_titles = []
                for root, directories, files in os.walk(folder_path):
                    for file in files:
                        if '.txt' in file:
                            curr_doc_titles.append(file.replace('.txt', ''))
                
                # Compare between current document list and saved document list.
                difference = list(set(curr_doc_titles) - set([doc.title for doc in self.__gui.corpus]))
                
                # Check if there is a difference between two document lists.
                if len(difference) == 0:
                    popup = WarningPopup(self.__gui, 'Updating an index',
                                         'The index is currently up to date!')
                    popup._start()
                else:
                    extended_corpus = []
                    for i in range(len(self.__gui.corpus), len(self.__gui.corpus) + len(difference)):
                        doc_id = 'doc_' + str(i)
                        doc_title = difference[i]
                        doc_content = open(folder_path + '\\' + difference[i] + '.txt', 'r', encoding='utf-8').read().replace('\n', '')
                        doc_i = Document(doc_id, doc_title, doc_content)
                        extended_corpus.append(doc_i)
                    
                    # Update the corpus and inverted index.
                    self.__gui.corpus = self.__gui.get_corpus() + extended_corpus
                    updating_thread = threading.Thread(target=self.__gui._update_inverted_index, args=(extended_corpus,), name='updating_thread')
                    updating_thread.start()
            except EnvironmentError:
                popup = WarningPopup(self.__gui, 'Updating an index',
                                     'The file path of the saved index does not exist!')
                popup._start()
        else:
            popup = WarningPopup(self.__gui, 'Updating an index',
                                 'There is no index to be updated!')
            popup._start()
    
    def __documentation(self):
        """
        The method to show documentation on GitHub.
        This feature is currently not available.

        Returns
        -------
        None.

        """
        webbrowser.open('https://github.com/williamo1099/Skripsi-2020')
        
    def __about(self):
        """
        The method to show an overview of the application.

        Returns
        -------
        None.

        """
        self.__about_window = AboutWindow(self.__gui)
        self.__about_window._start()