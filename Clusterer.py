
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt

class Clusterer:
    
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
        
        # Mendapatkan label cluster dari tiap dokumen teks.
        self.cluster_label = {}
        x_label = plt.gca().get_ymajorticklabels()
        for item in x_label:
            if item.get_color() not in self.cluster_label:
                self.cluster_label[item.get_color()] = []
            self.cluster_label[item.get_color()].append(item.get_text())
        
        # Mendapatkan tinggi dari dendrogram.
        dcoord_flat_list = []
        for item in dend['dcoord']:
            dcoord_flat_list += item
        self.dendrogram_height = max(dcoord_flat_list)
        
        return fig
    
    def get_dendrogram_height(self):
        return self.dendrogram_height
    
    def get_cluster(self):
        return self.cluster_label