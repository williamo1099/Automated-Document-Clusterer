
from retrieval.Document import Document
from retrieval.Indexer import Indexer
from gui.ToolTip import ToolTip

import os
import threading
import tkinter as tk
from tkinter import filedialog

class SearchFrame:
    
    def __init__(self, gui):
        """
        The constructor for SearchFrame class.

        Parameters
        ----------
        gui : gui
            The main gui.

        Returns
        -------
        None.

        """
        self.__gui = gui
        
        # Initialize the search frame in window.
        frame = tk.Frame(master=self.__gui.window)
        frame.pack(side='top', fill='x')
        frame.configure(background='white')
        
        # Initialize the folder entry in the frame.
        self.__folder_entry = tk.Entry(master=self.__gui.window)
        self.__folder_entry.pack(in_=frame, side='left', fill='x', expand='yes', padx=2, pady=2)
        self.__folder_entry.configure(state='disabled', background='white')
        
        # Initialize the select button in the frame.
        self.__select_button = tk.Button(master=self.__gui.window, text='Select folder', command=self.__select_folder)
        self.__select_button.pack(in_=frame, side='right', fill='x', padx=2, pady=2)
        self.__select_button.configure(background='white')
        ToolTip(self.__select_button, 'Select folder path containing the documents')
    
    def _restart(self):
        """
        The method to restore the frame's conditions to original.

        Returns
        -------
        None.

        """
        self._set_folder_entry('')
    
    def _set_folder_entry(self, folder_path):
        """
        The method to change folder path shown in folder entry.

        Parameters
        ----------
        folder_path : string
            The folder path.

        Returns
        -------
        None.

        """
        self.__folder_entry.configure(state='normal')
        self.__folder_entry.delete(0, 'end')
        self.__folder_entry.insert(0, folder_path)
        self.__folder_entry.configure(state='disabled')
    
    def __select_folder(self):
        """
        The method to select a folder containing documents to be clustered.

        Returns
        -------
        None.

        """
        folder_path = filedialog.askdirectory()
        self.__gui.folder_path = folder_path
        
        # Retrieve all .txt files in folder.
        doc_titles = []
        for root, directories, files in os.walk(folder_path):
            for file in files:
                if '.txt' in file:
                    doc_titles.append(os.path.join(root, file))
        corpus = []
        
        # Currently it is only compatible with Windows file system.
        escaped_folder_path = str(folder_path) + '\\'
        
        # Retrieve information of each documents.
        for i in range(0, len(doc_titles)):
            doc_id = 'doc_' + str(i)
            doc_title = os.path.splitext(doc_titles[i])[0].replace(escaped_folder_path, '')
            doc_content = open(doc_titles[i], 'r', encoding='utf-8').read().replace('\n', '')
            doc_i = Document(doc_id, doc_title, doc_content)
            corpus.append(doc_i)
        self.__gui.corpus = corpus
        
        # Build the inverted index.
        indexing_thread = threading.Thread(target=self.__build_inverted_index, name='indexing_thread')
        indexing_thread.start()
    
    def _update_inverted_index(self, inverted_index, extended_corpus):
        """
        The method to update the inverted index.

        Parameters
        ----------
        extended_corpus : list
            The list of newly added documents.

        Returns
        -------
        None.

        """
        self.__build_inverted_index(inverted_index, extended_corpus)
    
    def __build_inverted_index(self, inverted_index=None, extended_corpus=None):
        """
        The method to build an inverted index.
        
        Parameters
        ----------
        inverted_index : dictionary, optional
            The current inverted index (for updating). The default is None.
        extended_corpus : list, optional
            The list of new documents (for updating). The default is None.

        Returns
        -------
        dictionary
            The inverted index.

        """
        # Start progress bar, with value equals to 0.
        self.__gui._set_progress_value(0)
        
        stopwords_removal_option = self.__gui.preprocessor_option[0].get()
        stemming_option = self.__gui.preprocessor_option[1].get()
        case_folding_option = self.__gui.preprocessor_option[2].get()
        normalization_option = self.__gui.preprocessor_option[3].get()
        self.__gui._set_progress_value(5)
        
        indexer = Indexer(inverted_index)
        for doc in (self.__gui.corpus if extended_corpus is None else extended_corpus):
            indexer.index(doc, stopwords_removal_option, stemming_option, case_folding_option, normalization_option)
        inverted_index = indexer.inverted_index
        self.__gui.inverted_index = inverted_index
        
        # Set progress bar value to 50.
        self.__gui._set_progress_value(50)
        
        # Set progress value for each documents for vectorizing process.
        for doc in self.__gui.corpus:
            index = sorted(list(inverted_index.keys()), key=str.lower)
            corpus_size = len(self.__gui.corpus)
            doc.build_vector(inverted_index, index, corpus_size)
        
        # Set progress bar value to 95.
        self.__gui._set_progress_value(95)
        
        # Set the status to true, indicating that it is ready for clustering, and set progress bar value to 100, indicating the process has finished.
        self.__gui.cluster_status = True
        self.__gui._set_progress_value(100)