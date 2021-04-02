
from scipy.cluster.hierarchy import dendrogram
import matplotlib.pyplot as plt

class Dendrogram:
        
    def _plot_dendrogram(self, linkage, cut_off, labels, figsize=(10, 5), orientation='right'):
        """
        The method to plot dendrogram diagram.
        
        Parameters
        ----------
        linkage : array
            The linkage matrix.
        cut_off : float
            The cut-off height.
        labels : list
            The list of documents' title.
        figsize : tuple
            The size of the dendrogram figure. The default is [10, 5].
        orientation : string
            The figure orientation. The default is right.

        Returns
        -------
        fig : figure
            The figure of the dendrogram.

        """
        fig = plt.figure(figsize=figsize)
        self.__dend = dendrogram(linkage,
                    orientation=orientation,
                    color_threshold=cut_off,
                    labels=labels)
        
        # Cut the dendrogram at cut-off height.
        # Check whether the figure is shown horizontally or vertically.
        if figsize == (10, 5):
            plt.axvline(x=cut_off, linestyle='dashed')
        else:
            plt.axhline(y=cut_off, linestyle='dashed')
        return fig
    
    def _extract_clusters_by_color(self):
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
        for c, pi in zip(self.__dend['color_list'], self.__dend['icoord']):
            for leg in pi[1:3]:
                i = (leg - 5) / 10
                if abs(i - int(i)) <= 0:
                    if c not in cluster_list:
                        cluster_list[c] = []
                    cluster_list[c].append(self.__dend['ivl'][int(i)])
        return cluster_list