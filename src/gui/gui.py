
import os
import shutil
import pickle
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from retrieval.Document import Document
from retrieval.Indexer import Indexer
from clustering.Clusterer import Clusterer

from gui.WarningPopup import WarningPopup

class gui:
    
    def __init__(self):
        # Inisialisasi variable status.
        self.init_variable()
        
        # Inisialisasi window antarmuka program.
        self.window = tk.Tk()
        self.window.title('Automated Document Clustering')
        self.window.geometry('600x500')
        self.window.resizable(width=False,
                              height=False)
        
        # Membuat menu bar.
        self.create_menu_bar()
        # Membuat search frame.
        self.create_search_frame()
        # Membuat frame untuk proses clustering.
        self.create_cluster_frame()
        
    def init_variable(self):
        """
        Method untuk melakukan inisialisasi seluruh variable status.

        Returns
        -------
        None.

        """
        self.folder_path = '' # path folder corpus
        self.index = None # inverted index yang dibangun
        
        self.ready_status = False # apakah dendrogram siap digambar
        self.canvas_status = False # apakah dendrogram telah tergambar
        self.selected_method = None # metode pengelompokan yang digunakan
    
    def create_menu_bar(self):
        """
        Method untuk membuat menu bar pada gui.

        Returns
        -------
        None.

        """
        menu = tk.Menu(master=self.window)
        self.window.config(menu=menu)
        
        # Menambahkan menu file pada menu bar.
        file_menu = tk.Menu(menu)
        menu.add_cascade(label='File',
                         menu=file_menu)
        file_menu.add_command(label='New file',
                              command=self.reset_program)
        file_menu.add_command(label='Save index',
                              command=self.save_index)
        file_menu.add_command(label='Load index',
                              command=self.load_index)
        
        # Menambahkan menu help pada menu bar.
        help_menu = tk.Menu(menu)
        menu.add_cascade(label='Help',
                         menu=help_menu)
        help_menu.add_command(label='Tutorial')
        help_menu.add_command(label='Documentation')
    
    def create_search_frame(self):
        """
        Method untuk membuat search frame.
        Search frame adalah frame yang berkaitan dengan pengambilan dokumen teks.

        Returns
        -------
        None.

        """
        search_frame = tk.Frame(master=self.window)
        search_frame.pack(side='top',
                          fill='x')
        
        def select_folder():
            """
            Method untuk memilih path dari folder dokumen teks.
            Jika jumlah dokumen teks > 1, inverted index akan dibangun.
    
            Returns
            -------
            None.
    
            """
            self.reset_program()
            # Mengambil path folder dan mengisi entry folder path.
            self.folder_path = filedialog.askdirectory()
            self.set_folder_entry(self.folder_path)
            # Mengambil seluruh dokumen teks yang ada (dalam format .txt).
            doc_titles = []
            for root, directories, files in os.walk(self.folder_path):
                for file in files:
                    if '.txt' in file:
                        doc_titles.append(os.path.join(root, file))
            # Mengecek jumlah dokumen teks yang ada.
            if len(doc_titles) > 1:
                self.corpus = []
                escaped_folder_path = str(self.folder_path) + '\\'
                for i in range(0, len(doc_titles)):
                    doc_id = 'doc_' + str(i)
                    doc_title = os.path.splitext(doc_titles[i])[0].replace(escaped_folder_path, '')
                    doc_content = open(doc_titles[i], 'r', encoding='utf-8').read().replace('\n', '')
                    doc_i = Document(doc_id, doc_title, doc_content)
                    self.corpus.append(doc_i)
                # Membangun inverted index.
                if self.index is None:
                    indexer = Indexer()
                    for i in range(0, len(self.corpus)):
                        indexer.index(self.corpus[i])
                    self.index = indexer.get_inverted_index()
                # Set ready_status menjadi True, menandakan proses clustering siap untuk dilakukan.
                self.ready_status = True
            
        # Membuat entry untuk folder (menampilkan nama path folder).
        self.folder_entry = tk.Entry(master=self.window,
                                     width=50)
        self.folder_entry.pack(in_=search_frame,
                               side='left',
                               padx=2,
                               pady=2)
        self.folder_entry.configure(state='disabled')
        
        # Membuat button select untuk memilih folder.
        self.select_button = tk.Button(master=self.window,
                                  text='Select folder',
                                  command=select_folder)
        self.select_button.pack(in_=search_frame,
                           side='right',
                           padx=2,
                           pady=2)
        
    def create_cluster_frame(self):
        """
        Method untuk membuat cluster frame.
        Cluster frame adalah frame yang berkaitan dengan proses clustering.

        Returns
        -------
        None.

        """
        cluster_frame = tk.Frame(master=self.window)
        cluster_frame.pack(side='top')
        # Membuat combobox untuk memilih metode clustering.
        self.method_list = ['single', 'complete', 'average']
        self.method_combobox = ttk.Combobox(master=self.window,
                                   values=self.method_list)
        self.method_combobox.current(0)
        self.method_combobox.pack(in_=cluster_frame,
                           side='left',
                           padx=2,
                           pady=2)
        # Membuat button cluster untuk melakukan clustering.
        self.cluster_button = tk.Button(master=self.window,
                                   text='Cluster',
                                   command=self.cluster)
        self.cluster_button.pack(in_=cluster_frame,
                            side='right',
                            padx=2,
                            pady=2)
    
    def start(self):
        """
        Method untuk memulai menjalankan program.
        Tampilan antarmuka program akan ditampilkan.

        Returns
        -------
        None.

        """
        self.window.mainloop()
    
    def reset_program(self):
        """
        Method untuk melakukan reset keseluruhan program.
        Dengan reset, kondisi program akan menjadi seperti kondisi awal program.

        Returns
        -------
        None.

        """
        # Melihat apakah canvas sudah pernah digambar atau belum.
        if self.canvas_status is True:
            # Status True menandakan canvas sudah pernah digambar.
            self.reset_canvas()
            self.slider.destroy()
        
        # Menghapus seluruh isi variable yang ada.
        self.init_variable()
        # Menghapus isi dari entry folder path.
        self.set_folder_entry()

    def set_folder_entry(self, new_path=''):
        """
        Method untuk mengisi entry folder path.

        Parameters
        ----------
        new_path : string, optional
            Path folder yang baru. Nilai default adalah ''.

        Returns
        -------
        None.

        """
        self.folder_entry.configure(state='normal')
        self.folder_entry.delete(0, 'end')
        self.folder_entry.insert(0, new_path)
        self.folder_entry.configure(state='disabled')
        
    def cluster(self):
        """
        Method untuk mempersiapkan proses clustering.
        Persiapan dilakukan dengan mengecek apakah dokumen teks tersedia untuk dikelompokkan.

        Returns
        -------
        None.

        """
        # Melihat apakah proses clustering siap dilakukan.
        if self.ready_status is True:
            # Status True menandakan bahwa clustering siap dilakukan.
    
            def draw_canvas(cut_off=0):
                """
                Method untuk menggambarkan plot dalam canvas.
                Jika canvas sudah pernah digambar sebelumnya, isi canvas akan dihapus dahulu.
        
                Parameters
                ----------
                cut_off : float, optional
                    Ketinggian titik cut-off. Nilai default adalah 0.
        
                Returns
                -------
                None.
        
                """
                clusterer = Clusterer()
                fig = clusterer.cluster(self.index, self.corpus, self.method_list[self.method_combobox.current()], cut_off)
                fig.set_facecolor('#F0F0F0')
                # Melihat apakah canvas sudah pernah digambar atau belum.
                if self.canvas_status is True:
                    # Status true menandakan bahwa canvas sudah pernah digambar.
                    self.reset_canvas()
                else:
                    # Status false menandakan bahwa canvas belum pernah digambar.
                    # Menambahkan slider untuk mengatur ketinggian titik cut-off.
                    self.slider = tk.Scale(self.window,
                                      from_=0.0,
                                      to=clusterer.get_dendrogram_height(),
                                      resolution=0.01,
                                      variable=cut_off,
                                      command=lambda e:self.draw_canvas(self.slider.get()),
                                      orient='horizontal')
                    self.slider.pack(pady=5)
                    # Set status canvas jadi True, menandakan canvas sudah digambar.     
                    self.canvas_status = True
                # Menampilkan cophenet coefficient (sebagai evaluasi hasil pengelompokan).
                self.evaluation = tk.Label(master=self.window,
                                    text='Cophenet coefficient : ' + "{:.3f}".format(clusterer.get_cophenetcoeff()))
                self.evaluation.pack(pady=2)
                # Menggambar dendrogram (visualisasi hasil pengelompokan).
                self.canvas = FigureCanvasTkAgg(fig,
                                                master=self.window)
                self.canvas.draw()
                self.canvas.get_tk_widget().pack(pady=2)
                # Menambahkan frame result.
                self.result_frame = tk.Frame(self.window)
                self.result_frame.pack(side='top')
                # Menambahkan button organize.
                organize_button = tk.Button(master=self.window,
                                                 text='Organize documents',
                                                 command=lambda:self.organize_document(clusterer.get_cluster()))
                organize_button.pack(in_=self.result_frame,
                                     side='left',
                                     padx=5,
                                     pady=5)
                # Menambahkan button untuk download dendrogram.
                download_button = tk.Button(master=self.window,
                                            text='Download plot',
                                            command=lambda:self.save_plot(fig))
                download_button.pack(in_=self.result_frame,
                                     side='right',
                                     padx=5,
                                     pady=5)
            
            # Menggambarkan dendrogram.
            draw_canvas(0)
        else:
            popup = WarningPopup('Clustering process',
                                 'There are no documents to be indexed.')
            popup.show_popup()
    
    def reset_canvas(self):
        """
        Method untuk menghapus canvas yang telah digambarkan sebelumnya.
        Button organize, plot dan button download dalam canvas akan dihapus.

        Returns
        -------
        None.

        """
        self.result_frame.destroy()
        self.evaluation.destroy()
        self.canvas.get_tk_widget().destroy()
        
    def save_index(self):
        """
        Method untuk menyimpan inverted index yang telah dibangun.
        Inverted index disimpan dalam pickle.

        Returns
        -------
        None.

        """
        # Mengambil path untuk menyimpan file index.
        index_path = filedialog.asksaveasfilename(defaultextension='.pickle',
                                                  filetypes=(('pickle file', '*.pickle'),))
        # Melihat apakah index kosong atau tidak.
        if self.index is not None:
            # Menyimpan metadata.
            metadata = {}
            metadata['folder_path'] = self.folder_path
            metadata['corpus'] = self.corpus
            # Menyimpan keseluruhan data.
            data = {}
            data['index'] = self.index
            data['metadata'] = metadata
            with open(index_path, 'wb') as handle:
                pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
        else:
            # Menandakan bahwa tidak ada index yang disimpan.
            popup = WarningPopup('Saving an index',
                                 'There is no index to be saved!')
            popup.show_popup()

    def load_index(self):
        """
        Method untuk memuat inverted index yang telah disimpan sebelumnya.
        File yang diterima adalah file pickle (sesuai dengan penyimpanan).

        Returns
        -------
        None.

        """
        # Mengambil file path untuk index.
        index_path = filedialog.askopenfilename()
        try:
            with open(index_path, 'rb') as handle:
                data = pickle.load(handle)
                # Mengambil data inverted index.
                self.index = data['index']
                # Mengambil metadata yang tersimpan.
                metadata = data['metadata']
                self.folder_path = metadata['folder_path']
                self.set_folder_entry(self.folder_path)
                self.corpus = metadata['corpus']
                # Menandakan status ready menjadi True, menandakan proses clustering siap dilakukan.
                self.ready_status = True
                # Menampilkan pop-up warning yang memberi tahu bahwa index berhasil dimuat.
                popup = WarningPopup('Loading an index',
                                 'An index is successfully loaded!')
                popup.show_popup()
        except EnvironmentError:
            # Tidak ada file index yang dimuat.
            popup = WarningPopup('Loading an index',
                                 'There is no index to be loaded!')
            popup.show_popup()
    
    def save_plot(self, figure):
        """
        Method untuk menyimpan plot yang telah digambar.

        Parameters
        ----------
        figure : figure
            Gambar dendrogram.

        Returns
        -------
        None.

        """
        # Mengambil path untuk menyimpan file figure.
        figure_path = filedialog.asksaveasfilename(defaultextension='.png',
                                                  filetypes=(('PNG Image', '*.png'),))
        figure.savefig(figure_path)

    def organize_document(self, doc_label):
        """
        Method untuk mengelompokkan seluruh dokumen teks.
        Pengelompokan dilakukan dengan memasukkan setiap dokumen ke dalam folder cluster masing-masing.
        Hasil pengelompokan disimpan dalam satu folder organized.

        Parameters
        ----------
        doc_label : dictionary
            Daftar cluster dan isi dokumen teks di dalam cluster.
            Contohnya adalah {cluster1 : [doc1, doc2], cluster2 : [doc3]}.

        Returns
        -------
        None.

        """
        # Membuat sebuah folder bernama organized.
        folder = 'organized'
        organized_folder = os.path.join(self.folder_path, folder)
        if not os.path.exists(organized_folder):
            os.mkdir(organized_folder)
        # Mengelompokkan dokumen teks ke dalam folder cluster darinya.
        for label, doc in doc_label.items():
            # Membuat folder cluster.
            ci_folder = os.path.join(organized_folder, label)
            os.mkdir(ci_folder)
            for item in doc:
                # Menyalin dan memindahkan dokumen teks ke folder cluster.
                source = os.path.join(self.folder_path, item + '.txt')
                shutil.copyfile(source, ci_folder + '/' + item + '.txt')