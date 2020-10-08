
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt

class Clusterer:
    
    def set_dendrogram_height(self, dend):
        """
        Method untuk menghitung tinggi maksimal dari dendrogram.
        
        :param dend: dendrogram
        :type dend: dict
        """
        dcoord_flat_list = []
        for item in dend['dcoord']:
            dcoord_flat_list += item
        self.dendrogram_height = max(dcoord_flat_list)
    
    def get_dendrogram_height(self):
        """
        Method untuk mendapatkan tinggi maksimal dari dendrogram.
        
        :return dendrogram_height: tinggi maksimal dari dendrogram
        :type dendrogram_height: float64
        """
        return self.dendrogram_height
    
    def set_cluster(self, dend):
        """
        Method untuk mengelompokkan dokumen-dokumen teks yang ada.
        Proses pengelompokan dokumen teks dilakukan berdasarkan warna (berdasarkan titik cut-off).
        
        :param dend: dendrogram
        :type dend: dict
        """
        self.cluster_list = {}
        for c, pi in zip(dend['color_list'], dend['icoord']):
            for leg in pi[1:3]:
                i = (leg - 5) / 10
                if abs(i - int(i)) <= 0:
                    if c not in self.cluster_list:
                        self.cluster_list[c] = []
                    self.cluster_list[c].append(dend['ivl'][int(i)])
    
    def get_cluster(self):
        """
        Method untuk mendapatkan pengelompokan dokumen-dokumen teks.
        
        :return cluster_list: daftar cluster beserta dokumen teks anggotanya
        :type cluster_list: dict
        """
        return self.cluster_list
    
    def create_proximity_matrix(self, index, corpus):
        """
        Method untuk membangun matriks jarak untuk seluruh dokumen teks.
        Matriks jarak yang dibangun adalah matriks 1D salah satu sisi dari matriks jarak yang sesungguhnya.
        
        :param index: inverted index
        :type index: dict
        :param corpus: kumpulan dokumen teks
        :type corpus: list
        :return matrix: matriks jarak 1D
        :type matrix: list
        """
        # Untuk setiap dokumen teks yang ada, hitung vektor sebagai representasinya.
        for doc_i in corpus:
            doc_i.set_vector(index, len(corpus))
        
        # Berdasarkan vektor tersebut, akan dihitung jarak antar dokumen teks yang ada.
        matrix = []
        for i in range(1, len(corpus)):
            doc_i = corpus[i]
            for j in range(0, i):
                doc_j = corpus[j]
                distance = doc_i.count_distance(doc_j)
                matrix.append(distance)
        return matrix
    
    def cluster(self, index, corpus, cut_off=0.0):
        """
        Method untuk melakukan proses hierarchical clustering.
        Proses hierarchical clusteirng dilakukan berdasarkan matriks jarak yang telah dibangun.
        
        :param index: inverted index
        :type index: dict
        :param corpus: kumpulan dokumen teks
        :type corpus: list
        :param cut_off: ketinggian titik cut-off (default value=0)
        :type cut_off: float
        :return fig: dendrogram
        :type fig: matplotlib.figure.Figure
        """
        proximity_matrix = self.create_proximity_matrix(index, corpus)
        # Melakukan proses hierarchical clustering.
        # Metode yang digunakan adalah single-linkage.
        linked = linkage(proximity_matrix, method='single')
        
        # Menggambarkan dendrogram berdasarkan hasil hierarchical clustering.
        fig = plt.figure(figsize=(5, 5))
        dend = dendrogram(linked,
                    orientation='right',
                    color_threshold=cut_off,
                    labels=[doc.get_title() for doc in corpus])
        # Menggambarkan garis pemotong (cut-off).    
        plt.axvline(x=cut_off, linestyle='dashed')
        
        # Menyimpan daftar cluster beserta anggota-anggotanya.
        self.set_cluster(dend)
        # Menyimpan tinggi maksimal dari dendrogram yang dibangun.
        self.set_dendrogram_height(dend)
        return fig