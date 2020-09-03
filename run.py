
import os
import pickle
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Document import Document
from Indexer import Indexer
from Clusterer import Clusterer

def save_index(index):
    if index is not None:
        with open('index.pickle', 'wb') as handle:
            pickle.dump(index, handle, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        warning_popup = tk.Tk()
        warning_popup.wm_title('Saving an index')
        label = tk.Label(warning_popup, text='There is no index to save!')
        label.pack(side='top', fill='x', pady=10)
        ok_button = tk.Button(warning_popup, text='Ok', command=warning_popup.destroy)
        ok_button.pack()
        warning_popup.mainloop()

def load_index():
    with open('index.pickle', 'rb') as handle:
        global index
        index = pickle.load(handle)

def cluster():
    path = 'Document/'
    doc_titles = []
    for root, directories, files in os.walk(path):
        for file in files:
            if '.txt' in file:
                doc_titles.append(os.path.join(root, file))
    
    if len(doc_titles) > 1:
        corpus = []
        for i in range(0, len(doc_titles)):
            doc_id = 'doc_' + str(i)
            doc_content = open(doc_titles[i], 'r').read().replace('\n', '')
            doc_i = Document(doc_id, os.path.splitext(doc_titles[i])[0].replace(path, ''), doc_content)
            corpus.append(doc_i)
            
        # Build an inverted index.
        global index
        if index is None:
            indexer = Indexer()
            for i in range(0, len(corpus)):
                indexer.index(corpus[i])
            index = indexer.get_inverted_index(len(corpus))
        
        # Do document clustering.
        clusterer = Clusterer()
        fig = clusterer.cluster(index, corpus)
        
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack()
        
index = None

window = tk.Tk()
window.title('Document Clustering')
window.geometry("500x500")

menu = tk.Menu(window)
window.config(menu=menu)
file_menu = tk.Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Save index", command=lambda: save_index(index))
file_menu.add_command(label="Load index", command=load_index)

cluster_button = tk.Button(master=window, text='Cluster', command=cluster)
cluster_button.pack()
window.mainloop()