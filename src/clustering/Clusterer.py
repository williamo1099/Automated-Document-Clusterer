
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
        self.__corpus = corpus
        self.__distance_matrix = []
        self.__linkage = None
        self.__dendrogram = None
        
    def plot_dendrogram(self, cut_off=0, figsize=(10, 5), orientation='right'):
        """
        The method to get dendrogram figure.
        
        Parameters
        ----------
        cut_off : float, optional
            The cut-off height. The default is 0.
        figsize : tuple
            The size of the dendrogram figure. The default is (10, 5).
        orientation : string
            The dendrogram figure orientation. The default is right.

        Returns
        -------
        figure
            A figure of a dendrogram visualizing the result of clustering process.

        """
        return self.__dendrogram._plot_dendrogram(self.__linkage, cut_off, [doc.title for doc in self.__corpus], figsize, orientation) if self.__dendrogram is not None else None
    
    def cluster(self, method):
        """
        The method to do clustering process for documents in corpus.
        Algorithm used is agglomerative hierarchical clustering algorithm.

        Parameters
        ----------
        method : string
            The method used for calculating distances between two clusters.
            Possible values for this parameter are single, complete and average.

        Returns
        -------
        None.

        """
        # Set a 1-D condensed distance matrix.
        if self.__distance_matrix == []:
            self.__build_distance_matrix()
            
        # Set the linkage matrix as a result of the agglomerative hierarchical clustering process.
        if self.__linkage is None:
            self.__linkage = linkage(self.__distance_matrix,
                             method=method)
        self.__dendrogram = Dendrogram()    
    
    def __build_distance_matrix(self):
        """
        The method to build a 1-D condensed distance matrix.
        Each elements of the matrix is cosine distance between two documents in corpus.

        Returns
        -------
        None.

        """
        for i in range(0, len(self.__corpus)):
            doc_i = self.__corpus[i]
            for j in range(i + 1, len(self.__corpus)):
                doc_j = self.__corpus[j]
                distance = doc_i.calc_distance(doc_j)
                self.__distance_matrix.append(distance)
    
    def extract_clusters(self, dictionary=None, autorenaming_option=True):
        """
        The method to get a list of objects of each clusters obtained.
        Each cluster is named automatically based on most frequent terms (if autorenaming is True).
        
        Parameters
        ----------
        dictionary : list, optional
            The list of sorted terms. The default is None.
        autorenaming : boolean
            The autorenaming status. The default is True.

        Returns
        -------
        dictionary
            The list of objects of each clusters.
            Written as {cluster1: [doc1, doc2], cluster2: [doc3], etc.}.

        """
        cluster_list = self.__dendrogram._extract_clusters_by_color()
        return cluster_list if autorenaming_option is False else self.__autorename_clusters(cluster_list, dictionary, 5)
    
    def __autorename_clusters(self, cluster_list, dictionary, n=1):
        """
        The method to rename all clusters in cluster list based on most frequent terms.

        Parameters
        ----------
        cluster_list : dictionary
            The cluster result list which clusters are not named.
        dictionary : list
            The list of sorted terms.
        n : init
            The n-most common terms.

        Returns
        -------
        dictionary
            The list of objects of each now-renamed clusters.

        """
        renamed_cluster_list = {}
        for cluster, docs in cluster_list.items():
            list_of_vectors = []
            for doc_title in docs:
                for doc in self.__corpus:
                    if doc.title == doc_title:
                        list_of_vectors.append(doc.vector)
            
            def multiply_vector(vector):
                res = 1
                for dim in vector:
                    res *= dim
                return res
            
            # Calculate intersection between vectors.
            intersect = [multiply_vector(vector) for vector in zip(*list_of_vectors)]
            
            # Find common words between all documents.
            common_words = {}
            for i in range(0, len(intersect)):
                if intersect[i] != 0:
                    common_words[intersect[i]] = dictionary[i]
            
            # Sort common words.
            if (len(common_words) > 0):
                sorted_commond_words = sorted(common_words.items(), reverse=True)[:n]
                renamed_cluster_list[' '.join([str(elem) for elem in sorted_commond_words])] = cluster_list[cluster]
            else:
                renamed_cluster_list[cluster] = cluster_list[cluster]
        return renamed_cluster_list
    
    def calc_cophenetic_coeff(self):
        """
        The method to calculate a cophenetic coefficient correlation (CPCC) for the result obtained.
        The CPCC value can be used for an internal evaluation of the clusters.

        Returns
        -------
        c : float
            The copehenetic coefficient correlation (CPCC).

        """
        c, d = cophenet(self.__linkage, self.__distance_matrix)
        return round(c, 3)