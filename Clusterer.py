
import math
from scipy.spatial.distance import squareform
from scipy.cluster.hierarchy import dendrogram, linkage
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
        self.dend = dendrogram(linked,
                    orientation='right',
                    color_threshold=cut_off,
                    labels=[doc.get_title() for doc in corpus])
        return fig
    
    def get_dendrogram_height(self):
        flat_list = []
        for item in self.dend['dcoord']:
            flat_list += item
        return max(flat_list)