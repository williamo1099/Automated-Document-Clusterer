
from clustering.Dendrogram import Dendrogram

from scipy.cluster.hierarchy import linkage, cophenet

class Clusterer:
    
    def __init__(self, corpus):
        """
        The constructor for Clusterer class.

        Parameters
        ----------
        corpus : list
            The list of documents to be clustered.

        Returns
        -------
        None.

        """
        self.corpus = corpus
        self.distance_matrix = []
        
    def set_distance_matrix(self):
        """
        The method to build a 1-D condensed distance matrix.
        Each elements of the matrix is cosine distance between two documents in corpus.

        Returns
        -------
        None.

        """
        for i in range(0, len(self.corpus)):
            doc_i = self.corpus[i]
            for j in range(i + 1, len(self.corpus)):
                doc_j = self.corpus[j]
                distance = doc_i.calc_distance(doc_j)
                self.distance_matrix.append(distance)
        
    def cluster(self, method, cut_off=0):
        """
        The method to do clustering process for documents in corpus.
        Algorithm used is agglomerative hierarchical clustering algorithm.

        Parameters
        ----------
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
        # Set a 1-D condensed distance matrix.
        if self.distance_matrix == []:
            self.set_distance_matrix()
        
        # Set the linkage matrix as a result of the agglomerative hierarchical clustering process.
        self.linkage = linkage(self.distance_matrix,
                         method=method,
                         optimal_ordering=True)
        self.dendrogram = Dendrogram(self.linkage, [doc.get_title() for doc in self.corpus],
                                     cut_off)
        return self.dendrogram.plot_dendrogram()
    
    def extract_clusters(self):
        """
        The method to get a list of objects of each clusters obtained.

        Returns
        -------
        dictionary
            The list of objects of each clusters.
            Written as {cluster1: [doc1, doc2], cluster2: [doc3], etc.}..

        """
        return self.dendrogram.extract_clusters_by_color()
    
    def calc_cophenetic_coeff(self):
        """
        The method to calculate a cophenetic coefficient correlation (CPCC) for the result obtained.
        The CPCC value can be used for an internal evaluation of the clusters.

        Returns
        -------
        c : float
            The copehenetic coefficient correlation (CPCC).

        """
        c, d = cophenet(self.linkage, self.distance_matrix)
        return c
    
    def calc_f_score(self, benchmark):
        """
        The method to calculate an F-score for the result obtained.
        The F-score value can be used for an external evaluation of the clusters.

        Parameters
        ----------
        benchmark : dictionary
            A list of labels of each objects, used as a benchmark.

        Returns
        -------
        int
            The F-score.

        """
        return 0