
from retrieval.Document import Document
from retrieval.Indexer import Indexer
from gui.ToolTip import ToolTip

import os
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
        self.gui = gui
        
        # Initialize the search frame in window.
        search_frame = tk.Frame(master=self.gui.get_window())
        search_frame.pack(side='top', fill='x')
        search_frame.configure(background='white')
        
        # Initialize the folder entry in the frame.
        self.folder_entry = tk.Entry(master=self.gui.get_window(), width=50)
        self.folder_entry.pack(in_=search_frame, side='left', padx=2, pady=2)
        self.folder_entry.configure(state='disabled', background='white')
        
        # Initialize the select button in the frame.
        self.select_button = tk.Button(master=self.gui.get_window(), text='Select folder', command=self.select_folder)
        self.select_button.pack(in_=search_frame, side='right', padx=2, pady=2)
        self.select_button.configure(background='white')
        ToolTip(self.select_button, 'Select folder path containing the documents')
    
    def restart(self):
        """
        The method to restore the frame's conditions to original.

        Returns
        -------
        None.

        """
        self.set_folder_entry('')
    
    def set_folder_entry(self, folder_path):
        """
        The method to change folder path shown in folder entry.

        Parameters
        ----------
        folder_path : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.folder_entry.configure(state='normal')
        self.folder_entry.delete(0, 'end')
        self.folder_entry.insert(0, folder_path)
        self.folder_entry.configure(state='disabled')
    
    def select_folder(self):
        """
        The method to select a folder containing documents to be clustered.

        Returns
        -------
        None.

        """
        folder_path = filedialog.askdirectory()
        self.set_folder_entry(folder_path)
        self.gui.set_folder_path(folder_path)
        
        # Retrieve all .txt files in folder.
        doc_titles = []
        for root, directories, files in os.walk(folder_path):
            for file in files:
                if '.txt' in file:
                    doc_titles.append(os.path.join(root, file))
        corpus = []
        
        # Currently it is only compatible with MacOS file system.
        escaped_folder_path = str(folder_path) + '/'
        
        # Retrieve information of each documents.
        for i in range(0, len(doc_titles)):
            doc_id = 'doc_' + str(i)
            doc_title = os.path.splitext(doc_titles[i])[0].replace(escaped_folder_path, '')
            doc_content = open(doc_titles[i], 'r', encoding='utf-8').read().replace('\n', '')
            doc_i = Document(doc_id, doc_title, doc_content)
            corpus.append(doc_i)
        self.gui.set_corpus(corpus)
        
        # Build the inverted index.
        self.build_inverted_index()
    
    def build_inverted_index(self):
        """
        The method to build an inverted index.

        Parameters
        ----------
        corpus : list
            The list of documents.

        Returns
        -------
        dictionary
            The inverted index.

        """
        indexer = Indexer()
        for doc in self.gui.get_corpus():
            indexer.index(doc)
        inverted_index = indexer.get_inverted_index()
        self.gui.set_inverted_index(inverted_index)
        
        # Set the vector of each documents.
        for doc in self.gui.get_corpus():
            doc.set_vector(inverted_index)
        
        # Set the status to true, indicating that it is ready  for clustering.
        self.gui.set_cluster_status(True)