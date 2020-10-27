
from scipy.cluster.hierarchy import linkage, dendrogram, cophenet
import matplotlib.pyplot as plt

class Clusterer:
    
    def set_dendrogram_height(self, dend):
        """
        Method untuk menghitung tinggi maksimal dari dendrogram.

        Parameters
        ----------
        dend : dictionary
            Dendrogram visualisasi hasil pengelompokan.

        Returns
        -------
        None.

        """
        # Mengambil seluruh nilai dalam dcoord (menjadi flat array).
        dcoord_flat_list = []
        for item in dend['dcoord']:
            dcoord_flat_list += item
        # Mengambil nilai maksimal dari dcoord_flat_list.
        self.dendrogram_height = max(dcoord_flat_list)
    
    def get_dendrogram_height(self):
        """
        Method untuk mendapatkan tinggi maksimal dari dendrogram.

        Returns
        -------
        dendrogram_height : float
            Tinggi maksimal dari dendrogram.

        """
        return self.dendrogram_height
    
    def set_cluster(self, dend):
        """
        Method untuk mengelompokkan dokumen teks yang ada berdasarkan dendrogram.
        Pengelompokan dilakukan berdasarkan warna (berdasarkan ketinggian titik cut-off).
        Sumber : http://www.nxn.se/valent/extract-cluster-elements-by-color-in-python.

        Parameters
        ----------
        dend : dictionary
            Dendrogram visualisasi hasil pengelompokan.

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
        Method untuk mendapatkan pengelompokan dokumen teks.

        Returns
        -------
        cluster_list : dictionary
            Daftar cluster beserta dokumen teks anggotanya.
            Contohnya adalah {cluster1 : [doc1, doc2], cluster2 : [doc3]}.

        """
        return self.cluster_list
    
    def set_cophenet_coeff(self, proximity_matrix, linkage):
        """
        Method untuk menghitung nilai koefisien cophenet.
        Nilai koefisien cophenet digunakan sebagai evaluasi hasil pengelompokan.

        Parameters
        ----------
        proximity_matrix : list
            Matriks jarak 1D.
        linkage : array
            Pengelompokan dengan algoritma hierarchical clustering.

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
        cophenet_coeff : float
            Nilai koefisien cophenet sebagai evaluasi hasil pengelompokan.

        """
        return self.cophenet_coeff
    
    def create_proximity_matrix(self, index, corpus):
        """
        Method untuk membangun matriks jarak untuk seluruh dokumen teks.
        Matriks jarak yang dikembalikan adalah matriks jarak 1D (condensed proximity matrix).

        Parameters
        ----------
        index : dictionary
            Inverted index.
        corpus : list
            Daftar seluruh dokumen teks.

        Returns
        -------
        matrix : list
            Matriks jarak 1D.

        """
        # Menghitung representasi vektor masing-masing dokumen teks yang ada.
        for doc_i in corpus:
            doc_i.set_vector(index, len(corpus))
        # Menghitung matriks jarak berdasarkan representasi vektor.
        matrix = []
        for i in range(0, len(corpus)):
            doc_i = corpus[i]
            for j in range(i + 1, len(corpus)):
                doc_j = corpus[j]
                distance = doc_i.count_distance(doc_j)
                matrix.append(distance)
        return matrix
    
    def cluster(self, index, corpus, method, cut_off=0):
        """
        Method untuk melakukan proses hierarchical clustering.
        Proses dilakukan berdasarkan matriks jarak 1D.

        Parameters
        ----------
        index : dictionary
            Inverted index.
        corpus : list
            Daftar seluruh dokumen teks.
        method : string
            Nama metode yang akan digunakan (single, complete, average).
        cut_off : float, optional
            Ketinggian titik cut-off. Nilai default adalah 0.0.

        Returns
        -------
        fig : figure
            Dendrogram visualisasi hasil pengelompokan.

        """
        # Menghitung matriks jarak 1D.
        proximity_matrix = self.create_proximity_matrix(index, corpus)
        # Melakukan proses hierarchical clustering, dengan metode single-linkage.
        linked = linkage(proximity_matrix,
                         method=method,
                         optimal_ordering=True)
        # Menggambar dendrogram berdasarkan hasil hierarchical clustering.
        fig = plt.figure()
        dend = dendrogram(linked,
                    orientation='right',
                    color_threshold=cut_off,
                    labels=[doc.get_title() for doc in corpus])
        # Menggambarkan garis pemotong (cut-off).
        plt.axvline(x=cut_off, linestyle='dashed')
        # Mengatur agar plot tidak terpotong.
        plt.tight_layout()
        # Menyimpan daftar cluster beserta anggota-anggotanya.
        self.set_cluster(dend)
        # Menyimpan tinggi maksimal dari dendrogram yang dibangun.
        self.set_dendrogram_height(dend)
        # Menyimpan hasil evaluasi clustering dengan CPCC.
        self.set_cophenet_coeff(proximity_matrix, linked)
        return fig