
from scipy.cluster.hierarchy import dendrogram
import matplotlib.pyplot as plt

class Dendrogram:
    
    def __init__(self, linked, labels, cut_off):
        self.cut_off = cut_off
        self.dend = dendrogram(linked,
                    orientation='right',
                    color_threshold=cut_off,
                    labels=labels)
        
    def plot_dendrogram(self):
        """
        Plot dendrogram diagram.

        Returns
        -------
        fig : figure
            A figure of the dendrogram.

        """
        fig = plt.figure(figsize=(10, 5))
        dendrogram = self.dend
        
        # Cut the dendrogram at cut_off height.
        # If the cut-off height equals to 0, there will be no cut-off line.
        plt.axvline(x=self.cut_off, linestyle='dashed')
        return fig
    
    def extract_clusters_by_color(self):
        """
        Extract a list of objects of each clusters in a dendrogram based on colors.
        Shout out to http://www.nxn.se/valent/extract-cluster-elements-by-color-in-python.
        
        Returns
        -------
        cluster_list : dictionary
            A list of objects of each clusters.
            Written as {cluster1: [doc1, doc2], cluster2: [doc3], etc.}.

        """
        cluster_list = {}
        for c, pi in zip(self.dend['color_list'], self.dend['icoord']):
            for leg in pi[1:3]:
                i = (leg - 5) / 10
                if abs(i - int(i)) <= 0:
                    if c not in self.cluster_list:
                        cluster_list[c] = []
                    cluster_list[c].append(self.dend['ivl'][int(i)])
        return cluster_list