
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
    
    def cluster(self, index, corpus):
        proximity_matrix = self.create_proximity_matrix(index, corpus)
        linked = linkage(squareform(proximity_matrix), method='single', metric='cosine')
        plt.figure(figsize=(10, 7))
        dendrogram(linked,
                    orientation='right',
                    labels=[doc.get_title() for doc in corpus])
        plt.show()