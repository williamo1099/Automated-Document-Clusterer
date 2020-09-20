
import os
import pickle
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Document import Document
from Indexer import Indexer
from Clusterer import Clusterer

class gui:
    
    def __init__(self):
        self.index = None # Inverted index.
        self.ready_status = False # Status yang menunjukkan proses cluster siap dilakukan tanpa melakukan proses indexing.
        self.canvas_status = False # Status yang menunjukkan canvas sudah tergambar atau belum.
        
        self.window = tk.Tk()
        self.window.title('Document Clustering')
        self.window.geometry('500x500')
        
        # Menu bar.
        menu = tk.Menu(self.window)
        self.window.config(menu=menu)
        # Menu file.
        file_menu = tk.Menu(menu)
        menu.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Save index', command=self.save_index)
        file_menu.add_command(label='Load index', command=self.load_index)
        
        # Button untuk cluster.
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
            # Menyimpan data-data (selain indeks) yang dibutuhkan.
            metadata = {}
            metadata['corpus'] = self.corpus
            
            data = {}
            data['index'] = self.index
            data['metadata'] = metadata
            with open(index_path, 'wb') as handle:
                pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            self.show_warning_popup('Saving an index', 'There is no index to be saved!')

    def load_index(self):
        index_path = filedialog.askopenfilename()
        try:
            with open(index_path, 'rb') as handle:
                data = pickle.load(handle)
                # Mengambil inverted index yang telah di-load.
                self.index = data['index']
                # Mengambil data-data (selain indeks) yang dibutuhkan.
                metadata = data['metadata']
                self.corpus = metadata['corpus']
                # Menandakan status sebagai True.
                self.ready_status = True
                self.show_warning_popup('Loading an index', 'An index is successfully loaded!')
        except EnvironmentError:
            self.show_warning_popup('Loading an index', 'There is no index to be loaded!')
    
    def organize_document(self, lst):
        print(lst)
    
    def cluster(self):
        # Ketika status False, harus dilakukan proses indexing yang digunakan untuk di-cluster.
        if self.ready_status is False:
            folder_path = filedialog.askdirectory()
            doc_titles = []
            for root, directories, files in os.walk(folder_path):
                for file in files:
                    if '.txt' in file:
                        doc_titles.append(os.path.join(root, file))
            
            if len(doc_titles) > 1:
                self.corpus = []
                for i in range(0, len(doc_titles)):
                    doc_id = 'doc_' + str(i)
                    doc_content = open(doc_titles[i], 'r').read().replace('\n', '')
                    doc_i = Document(doc_id, os.path.splitext(doc_titles[i])[0].replace(folder_path, ''), doc_content)
                    self.corpus.append(doc_i)
                    
                # Membangun inverted index berdasarkan dokumen teks dalam corpus.
                if self.index is None:
                    indexer = Indexer()
                    for i in range(0, len(self.corpus)):
                        indexer.index(self.corpus[i])
                    self.index = indexer.get_inverted_index(len(self.corpus))
                
                # Melakukan proses clustering dan menggambarkan dendrogram.
                self.draw_canvas(0)
        else:
            # Status True menandakan indeks sudah di-load dan siap untuk melakukan proses clustering.
            self.draw_canvas(0)
        
    def draw_canvas(self, cut_off=0):
        clusterer = Clusterer()
        fig = clusterer.cluster(self.index, self.corpus, cut_off)
        
        # Ketika status True, canvas sudah pernah digambar dan harus dihapus.
        if self.canvas_status is True:
            self.organize_button.destroy()
            self.canvas.get_tk_widget().destroy()
        else:
            # Menambahkan slider (untuk keperluan cut-off).
            slider = tk.Scale(self.window,
                              from_=0.0,
                              to=clusterer.get_dendrogram_height(),
                              resolution=0.01,
                              variable=cut_off,
                              command=lambda e:self.draw_canvas(slider.get()),
                              orient='horizontal')
            slider.pack()            
            self.canvas_status = True
        
        # Menambahkan button organize.
        self.organize_button = tk.Button(master=self.window,
                                    text='Organize',
                                    command=lambda:self.organize_document(clusterer.get_cluster()))
        self.organize_button.pack()
        
        # Menggambar dendrogram.
        self.canvas = FigureCanvasTkAgg(fig, master=self.window)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack()