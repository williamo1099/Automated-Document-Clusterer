
from scipy.cluster.hierarchy import linkage, dendrogram, cophenet
import matplotlib.pyplot as plt

class Clusterer:
    
    def set_dendrogram_height(self, dend):
        """
        Method untuk menghitung tinggi maksimal dari dendrogram.

        Parameters
        ----------
        dend : dict
            Dendrogram sebagai visualisasi hasil pengelompokan.

        Returns
        -------
        None.

        """
        dcoord_flat_list = []
        for item in dend['dcoord']:
            dcoord_flat_list += item
        self.dendrogram_height = max(dcoord_flat_list)
    
    def get_dendrogram_height(self):
        """
        Method untuk mendapatkan tinggi maksimal dari dendrogram.

        Returns
        -------
        dendrogram_height : float64
            Tinggi maksimal dari dendrogram.

        """
        return self.dendrogram_height
    
    def set_cluster(self, dend):
        """
        Method untuk mengelompokkan dokumen-dokumen teks yang ada.
        Proses pengelompokan dokumen teks dilakukan berdasarkan warna (berdasarkan titik cut-off).

        Parameters
        ----------
        dend : dict
            Dendrogram sebagai visualisasi hasil pengelompokan.

        Returns
        -------
        None.

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

        Returns
        -------
        cluster_list : dict
            Daftar cluster beserta dokumen teks anggotanya.

        """
        return self.cluster_list
    
    def set_cophenet_coeff(self, proximity_matrix, linkage):
        """
        Method untuk menghitung nilai koefisien cophenet.

        Parameters
        ----------
        proximity_matrix : list
            Matriks jarak 1D.
        linkage : numpy.ndarray
            Hasil pengelompokan dengan algoritma hierarchical clustering.

        Returns
        -------
        None.

        """
        c, d = cophenet(linkage, proximity_matrix)
        self.cophenet_coeff = c
    
    def get_cophenetcoeff(self):
        """
        Method untuk mendapatkan nilai koefisien cophenet.

        Returns
        -------
        cophenet_coeff : numpy.ndarray
            Nilai koefisien cophenet.

        """
        return self.cophenet_coeff
    
    def create_proximity_matrix(self, index, corpus):
        """
        Method untuk membangun matriks jarak untuk seluruh dokumen teks.
        Matriks jarak yang dibangun adalah matriks 1D salah satu sisi dari matriks jarak yang sesungguhnya.

        Parameters
        ----------
        index : dict
            Inverted index yang menyimpan pemetaan term ke lokasi term tersebut berada.
        corpus : list
            Daftar seluruh dokumen teks.

        Returns
        -------
        matrix : list
            Matriks jarak 1D.

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
    
    def cluster(self, index, corpus, cut_off=0):
        """
        Method untuk melakukan proses hierarchical clustering.
        Proses hierarchical clusteirng dilakukan berdasarkan matriks jarak yang telah dibangun.

        Parameters
        ----------
        index : dict
            Inverted index yang menyimpan pemetaan term ke lokasi term tersebut berada.
        corpus : list
            Daftar seluruh dokumen teks.
        cut_off : float, optional
            Ketinggian titik cut-off. The default is 0.

        Returns
        -------
        fig : matplotlib.figure.Figure
            Dendrogram sebagai visualisasi hasil pengelompokan.

        """
        proximity_matrix = self.create_proximity_matrix(index, corpus)
        # Melakukan proses hierarchical clustering.
        # Metode yang digunakan adalah single-linkage.
        linked = linkage(proximity_matrix, method='single', metric='cosine')
        
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
        # Menyimpan hasil evaluasi clustering dengan CPCC.
        self.set_cophenet_coeff(proximity_matrix, linked)
        return fig