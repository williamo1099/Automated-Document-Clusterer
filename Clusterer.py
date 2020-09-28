
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt

class Clusterer:
    
    def set_dendrogram_height(self, dend):
        dcoord_flat_list = []
        for item in dend['dcoord']:
            dcoord_flat_list += item
        self.dendrogram_height = max(dcoord_flat_list)
    
    def get_dendrogram_height(self):
        return self.dendrogram_height
    
    def set_cluster(self, dend):
        self.cluster_list = {}
        for c, pi in zip(dend['color_list'], dend['icoord']):
            for leg in pi[1:3]:
                i = (leg - 5) / 10
                if abs(i - int(i)) <= 0:
                    if c not in self.cluster_list:
                        self.cluster_list[c] = []
                    self.cluster_list[c].append(dend['ivl'][int(i)])
    
    def get_cluster(self):
        return self.cluster_list
    
    def create_proximity_matrix(self, index, corpus):
        for doc_i in corpus:
            doc_i.set_weighting_list(index, len(corpus))
            
        matrix = []
        for i in range(1, len(corpus)):
            doc_i = corpus[i]
            for j in range(0, i):
                doc_j = corpus[j]
                distance = doc_i.count_distance(doc_j)
                matrix.append(distance)
        return matrix
    
    def cluster(self, index, corpus, cut_off=0):
        proximity_matrix = self.create_proximity_matrix(index, corpus)
        linked = linkage(proximity_matrix, method='single', metric='cosine')
        fig = plt.figure(figsize=(5, 5))
        dend = dendrogram(linked,
                    orientation='right',
                    color_threshold=cut_off,
                    labels=[doc.get_title() for doc in corpus])
        # Menggambarkan cut-off.        
        plt.axvline(x=cut_off, linestyle='dashed')
        # Mendapatkan label cluster dari tiap dokumen teks.  
        self.set_cluster(dend)
        # Mendapatkan tinggi dari dendrogram.
        self.set_dendrogram_height(dend)
        return fig