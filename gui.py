
import os
import shutil
import pickle
import tkinter as tk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Document import Document
from Indexer import Indexer
from Clusterer import Clusterer

class gui:
    
    def __init__(self):
        self.reset_variable()
        # Inisialisasi window antarmuka program.
        self.window = tk.Tk()
        self.window.title('Automated Document Clustering')
        self.window.geometry('500x600')
        self.window.resizable(width=False,
                              height=False)        
        # Membuat menu bar.
        menu = tk.Menu(self.window)
        self.window.config(menu=menu)
        # Menambahkan menu file pada menu bar.
        file_menu = tk.Menu(menu)
        menu.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='New file',
                              command=self.reset_program)
        file_menu.add_command(label='Save index',
                              command=self.save_index)
        file_menu.add_command(label='Load index',
                              command=self.load_index)
        # Membuat frame untuk proses pengambilan path folder dokumen teks.
        search_frame = tk.Frame(self.window)
        search_frame.pack(side='top')
        self.folder_entry = tk.Entry(self.window,
                                     width=65)
        self.folder_entry.pack(in_=search_frame,
                               side='left',
                               padx=2,
                               pady=2)
        self.folder_entry.configure(state='disabled')
        select_button = tk.Button(self.window,
                                  text='Select folder',
                                  command=self.select_folder)
        select_button.pack(in_=search_frame,
                           side='right',
                           padx=2,
                           pady=2)
        # Membuat button untuk melakukan proses clustering.
        cluster_button = tk.Button(master=self.window,
                                   text='Cluster',
                                   command=self.cluster)
        cluster_button.pack()
        
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
        self.reset_variable()
        # Menghapus isi dari entry folder path.
        self.reset_folder_entry()

    def reset_variable(self):
        """
        Method untuk melakukan reset terhadap seluruh variable status yang telah disimpan.
        Variable folder_path menyimpan path folder berisi dokumen teks yang dikelompokkan.
        Variable index menyimpan inverted index yang telah dibangun.
        Variable ready_status menandakan apakah dendrogram siap untuk digambarkan dalam canvas.
        Variable canvas_status menandakan apakah dnedrogram telah tergambar dalam canvas.

        Returns
        -------
        None.

        """
        self.folder_path = ''
        self.index = None
        self.ready_status = False
        self.canvas_status = False
    
    def select_folder(self):
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
        self.reset_folder_entry(self.folder_path)
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
                doc_content = open(doc_titles[i], 'r').read().replace('\n', '')
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

    def reset_folder_entry(self, new_path=''):
        """
        Method untuk melakukan reset terhadap isi entry folder path.

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
            self.draw_canvas(0)
        else:
            self.show_warning_popup('Clustering process', 'There are no documents to be indexed.') 

    def draw_canvas(self, cut_off=0):
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
        fig = clusterer.cluster(self.index, self.corpus, cut_off)
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
            # Menampilkan cophenet coefficient (sebagai evaluasi hasil pengelompokan).
            self.evaluation = tk.Label(master=self.window,
                                text='Cophenet coefficient : ' + str(clusterer.get_cophenetcoeff()))
            self.evaluation.pack(pady=2)
            # Set status canvas jadi True, menandakan canvas sudah digambar.     
            self.canvas_status = True
        # Menggambar dendrogram (visualisasi hasil pengelompokan).
        self.canvas = FigureCanvasTkAgg(fig, master=self.window)
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
    
    def show_warning_popup(self, title, msg):
        """
        Method untuk menampilkan sebuah pop-up warning.

        Parameters
        ----------
        title : string
            Judul dari pop-up warning.
        msg : string
            Isi pesan dari pop-up warning.

        Returns
        -------
        None.

        """
        warning_popup = tk.Tk()
        warning_popup.wm_title(title)
        label = tk.Label(warning_popup,
                         text=msg)
        label.pack(side='top',
                   fill='x',
                   pady=10)
        ok_button = tk.Button(warning_popup,
                              text='Ok',
                              command=warning_popup.destroy)
        ok_button.pack()
        # Menampilkan pop-up warning.
        warning_popup.mainloop()
        
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
            self.show_warning_popup('Saving an index', 'There is no index to be saved!')

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
                self.corpus = metadata['corpus']
                # Menandakan status ready menjadi True, menandakan proses clustering siap dilakukan.
                self.ready_status = True
                # Menampilkan pop-up warning yang memberi tahu bahwa index berhasil dimuat.
                self.show_warning_popup('Loading an index', 'An index is successfully loaded!')
        except EnvironmentError:
            # Tidak ada file index yang dimuat.
            self.show_warning_popup('Loading an index', 'There is no index to be loaded!')
    
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