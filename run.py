
import os
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Document import Document
from Indexer import Indexer
from Clusterer import Clusterer

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
        
window = tk.Tk()
window.title('Document Clustering')
window.geometry("500x500")
cluster_button = tk.Button(master=window, text='Cluster', command=cluster)
cluster_button.pack()
window.mainloop()