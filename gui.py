
import os
import pickle
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Document import Document
from Indexer import Indexer
from Clusterer import Clusterer

class gui:
    
    def __init__(self, title, size):
        self.index = None
        
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry(size)
        
        # File menu.
        menu = tk.Menu(self.window)
        self.window.config(menu=menu)
        file_menu = tk.Menu(menu)
        menu.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Save index', command=self.save_index)
        file_menu.add_command(label='Load index', command=self.load_index)
        
        # Cluster button.
        cluster_button = tk.Button(master=self.window, text='Cluster', command=self.cluster)
        cluster_button.pack()
        
    def start(self):
        self.window.mainloop()
        
    def show_warning_popup(self, title, msg):
        warning_popup = tk.Tk()
        warning_popup.wm_title(title)
        label = tk.Label(warning_popup, text=msg)
        label.pack(side='top', fill='x', pady=10)
        ok_button = tk.Button(warning_popup, text='Ok', command=warning_popup.destroy)
        ok_button.pack()
        warning_popup.mainloop()
    
    def save_index(self):
        index_path = filedialog.asksaveasfilename(defaultextension='.pickle',
                                                  filetypes=(('pickle file', '*.pickle'),))
        if self.index is not None:
            with open(index_path, 'wb') as handle:
                pickle.dump(self.index, handle, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            self.show_warning_popup('Saving an index', 'There is no index to be saved!')

    def load_index(self):
        index_path = filedialog.askopenfilename()
        try:
            with open(index_path, 'rb') as handle:
                self.index = pickle.load(handle)
                self.show_warning_popup('Loading an index', 'An index is successfully loaded!')
        except EnvironmentError:
            self.show_warning_popup('Loading an index', 'There is no index to be loaded!')
    
    def cluster(self):
        folder_path = 'Document/'
        # folder_path = filedialog.askdirectory()
        doc_titles = []
        for root, directories, files in os.walk(folder_path):
            for file in files:
                if '.txt' in file:
                    doc_titles.append(os.path.join(root, file))
        
        if len(doc_titles) > 1:
            corpus = []
            for i in range(0, len(doc_titles)):
                doc_id = 'doc_' + str(i)
                doc_content = open(doc_titles[i], 'r').read().replace('\n', '')
                doc_i = Document(doc_id, os.path.splitext(doc_titles[i])[0].replace(folder_path, ''), doc_content)
                corpus.append(doc_i)
                
            # Build an inverted index.
            if self.index is None:
                indexer = Indexer()
                for i in range(0, len(corpus)):
                    indexer.index(corpus[i])
                self.index = indexer.get_inverted_index(len(corpus))
            
            # Do document clustering.
            clusterer = Clusterer()
            fig = clusterer.cluster(self.index, corpus)
            
            canvas = FigureCanvasTkAgg(fig, master=self.window)
            canvas.draw()
            canvas.get_tk_widget().pack()