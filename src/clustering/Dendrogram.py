
from scipy.cluster.hierarchy import dendrogram
import matplotlib.pyplot as plt

class Dendrogram:
    
    def __init__(self, linked, cut_off):
        """
        The constructor for Dendrogram class.

        Parameters
        ----------
        linked : array
            The linkage matrix.
        cut_off : float
            The cut-off height.

        Returns
        -------
        None.

        """
        self.linked = linked
        self.cut_off = cut_off
        
    def plot_dendrogram(self, labels=None):
        """
        The method to plot dendrogram diagram.
        
        Parameters
        ----------
        labels : list
            The list of documents' title. The default is None.

        Returns
        -------
        fig : figure
            The figure of the dendrogram.

        """
        fig = plt.figure(figsize=(10, 5))
        self.dend = dendrogram(self.linked,
                    orientation='right',
                    color_threshold=self.cut_off,
                    labels=labels)
        
        # Cut the dendrogram at cut-off height.
        # If the cut-off height equals to 0, there will be no cut-off line.
        plt.axvline(x=self.cut_off, linestyle='dashed')
        return fig
    
    def extract_clusters_by_color(self):
        """
        The method to extract a list of objects of each clusters in the dendrogram based on colors.
        Shout out to http://www.nxn.se/valent/extract-cluster-elements-by-color-in-python.
        
        Returns
        -------
        cluster_list : dictionary
            The list of objects of each clusters.
            Written as {cluster1: [doc1, doc2], cluster2: [doc3], etc.}.

        """
        cluster_list = {}
        for c, pi in zip(self.dend['color_list'], self.dend['icoord']):
            for leg in pi[1:3]:
                i = (leg - 5) / 10
                if abs(i - int(i)) <= 0:
                    if c not in cluster_list:
                        cluster_list[c] = []
                    cluster_list[c].append(self.dend['ivl'][int(i)])
        return cluster_list