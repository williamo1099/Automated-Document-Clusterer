
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import fcluster, dendrogram, linkage
import matplotlib.pyplot as plt

class Clusterer:
    
    def create_proximity_matrix(self, index, corpus):
        matrix = []
        for doc_i in corpus:
            distance_list = []
            for doc_j in corpus:
                distance_list.append(doc_i.count_distance(doc_j, index, len(corpus)))
            matrix.append(distance_list)
        return matrix
    
    def cluster(self, index, corpus, cut_off=0):
        proximity_matrix = self.create_proximity_matrix(index, corpus)
        linked = linkage(squareform(proximity_matrix), method='single', metric='cosine')
        fig = plt.figure(figsize=(5, 5))
        dend = dendrogram(linked,
                    orientation='right',
                    color_threshold=cut_off,
                    labels=[doc.get_title() for doc in corpus])
        
        # Mendapatkan label cluster dari tiap dokumen teks.
        # self.cluster_label = fcluster(linked, cut_off, criterion='distance')
        print(dend)
        # Mendapatkan tinggi dari dendrogram.
        dcoord_flat_list = []
        for item in dend['dcoord']:
            dcoord_flat_list += item
        self.dendrogram_height = max(dcoord_flat_list)

        return fig
    
    def get_dendrogram_height(self):
        return self.dendrogram_height
    
    def get_cluster(self):
        # return self.cluster_label
        return 0