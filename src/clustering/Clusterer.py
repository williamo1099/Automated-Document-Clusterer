
from clustering.Dendrogram import Dendrogram

from scipy.cluster.hierarchy import linkage, dendrogram, cophenet
import matplotlib.pyplot as plt

class Clusterer:
    
    def __init__(self, corpus):
        self.corpus = corpus
        self.proximity_matrix = []
    
    def get_cluster(self):
        """
        Get a list of objects of each clusters.

        Returns
        -------
        dictionary
            A list of objects of each clusters.
            Written as {cluster1: [doc1, doc2], cluster2: [doc3], etc.}..

        """
        return self.dendrogram.extract_clusters_by_color()
    
    def get_cophenetic_coeff(self):
        """
        Count the cophenetic coefficient correlation (CPCC) for the result get.
        The CPCC value can be used for an internal evaluation of the clusters.

        Returns
        -------
        c : float
            The copehenetic coefficient correlation (CPCC).

        """
        c, d = cophenet(self.linked, self.distance_matrix)
        return c
    
    def set_distance_matrix(self, index):
        """
        Build a 1-D condensed distance matrix consisting cosine distances between documents in corpus.

        Parameters
        ----------
        index : dictionary
            An inverted index.

        Returns
        -------
        None.

        """
        # Set each documents' vector representation.
        for doc_i in self.corpus:
            doc_i.set_vector(index, len(self.corpus))
            
        # Build a 1-D condensed distance matrix.
        for i in range(0, len(self.corpus)):
            doc_i = self.corpus[i]
            for j in range(i + 1, len(self.corpus)):
                doc_j = self.corpus[j]
                distance = doc_i.count_distance(doc_j)
                self.proximity_matrix.append(distance)
    
    def cluster(self, index, method, cut_off=0):
        """
        Do the agglomerative hierarchical clustering process for the given documents in corpus.

        Parameters
        ----------
        index : dictionary
            An inverted index.
        method : string
            The method used for calculating distances between two clusters.
            Possible values for this parameter are single, complete and average.
        cut_off : float, optional
            The height of a cut-off point. The default is 0.

        Returns
        -------
        figure
            A figure of a dendrogram visualizing the result of clustering process.

        """
        # Set a 1-D condensed distance amtrix.
        self.set_distance_matrix(index)
        
        # Set the linkage matrix as a result of the agglomerative hierarchical clustering process.
        self.linked = linkage(self.proximity_matrix,
                         method=method,
                         optimal_ordering=True)
        
        dend = dendrogram(self.linked,
                    orientation='right',
                    color_threshold=cut_off,
                    labels=[doc.get_title() for doc in self.corpus])
        self.dendrogram = Dendrogram(dend)
        return self.dendrogram.plot_dendrogram()