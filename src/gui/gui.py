
from gui.MenuBar import MenuBar
from gui.SearchFrame import SearchFrame
from gui.ClusterFrame import ClusterFrame
from gui.ProgressFrame import ProgressFrame

import tkinter as tk

class gui:
    
    def __init__(self):
        """
        The constructor for gui class.

        Returns
        -------
        None.

        """
        # Initialize all variables.
        self.cluster_status = False
        self.canvas_status = False
        self.cut_status = False
        self.folder_path = ''
        self.corpus = []
        self.inverted_index = None
        
        # Initialize the application's gui.
        self.window = tk.Tk()
        self.window.title('Automated Document Clusterer')
        self.window.tk.call('wm', 'iconphoto', self.window._w, tk.PhotoImage(file='resources/logo25.png'))
        self.window.geometry('750x450')
        self.window.resizable(width=False, height=False)
        self.window.configure(background='white')
        
        # Initialize the menu bar.
        self.menu_bar = MenuBar(self)
        
        # Initialiaze all frames in the window.
        self.search_frame = SearchFrame(self)
        self.cluster_frame = ClusterFrame(self)
        self.progress_frame = ProgressFrame(self)
        
    def start(self):
        """
        The method to start application's gui.

        Returns
        -------
        None.

        """
        self.window.mainloop()
        
    def restart(self):
        """
        The method to restore application's conditions to original.

        Returns
        -------
        None.

        """
        # Restart all frames contained in window.
        self.search_frame.restart()
        self.cluster_frame.restart()
        
        # Reinitialize all variables.
        self.cluster_status = False
        self.canvas_status = False
        self.folder_path = ''
        self.corpus = []
        self.inverted_index = None
        
    def set_progress_value(self, value):
        """
        The method to set the progress bar value.

        Parameters
        ----------
        value : int
            The progress bar value.

        Returns
        -------
        None.

        """
        self.progress_frame.update_progress_bar(value)
    
    def get_window(self):
        """
        The method to get the main gui window.

        Returns
        -------
        Tk Interface
            The main gui window.

        """
        return self.window
    
    def get_cluster_status(self):
        """
        The method to get the cluster status.
        Cluster status indicates whether it is ready to do clustering process or not.

        Returns
        -------
        boolean
            The cluster status.

        """
        return self.cluster_status
    
    def set_cluster_status(self, cluster_status):
        """
        THe method to set the cluster status.

        Parameters
        ----------
        cluster_status : boolean
            The cluster status.

        Returns
        -------
        None.

        """
        self.cluster_status = cluster_status
    
    def get_canvas_status(self):
        """
        The method to get the canvas status.
        Canvas status indicates whether it is ready to draw on canvas or not.

        Returns
        -------
        boolean
            The canvas status.

        """
        return self.canvas_status
    
    def set_canvas_status(self, canvas_status):
        """
        The method to set the canvas status.

        Parameters
        ----------
        canvas_status : boolean
            The canvas status.

        Returns
        -------
        None.

        """
        self.canvas_status = canvas_status
        
    def get_cut_status(self):
        """
        The method to get the cut-off status.
        Cut-off status indicates whether it is ready to cut the dendrogram or not.

        Returns
        -------
        boolean
            The cut-off status.

        """
        return self.cut_status
    
    def set_cut_status(self, cut_status):
        """
        THe method to set the cut-off status.

        Parameters
        ----------
        cut_status : boolean
            The cut-off status.

        Returns
        -------
        None.

        """
        self.cut_status = cut_status
        
    def get_folder_path(self):
        """
        The method to get the folder path of corpus.

        Returns
        -------
        string
            The folder path.

        """
        return self.folder_path
    
    def set_folder_path(self, folder_path):
        """
        The method to set the folder path of corpus.
        This automatically set the folder entry to current folder path.

        Parameters
        ----------
        folder_path : string
            The folder path.

        Returns
        -------
        None.

        """
        self.folder_path = folder_path
        self.search_frame.set_folder_entry(folder_path)
        
    def get_corpus(self):
        """
        The method to get corpus.

        Returns
        -------
        list
            The list of documents.

        """
        return self.corpus
    
    def set_corpus(self, corpus):
        """
        The method to set corpus.

        Parameters
        ----------
        corpus : list
            The list of documents.

        Returns
        -------
        None.

        """
        self.corpus = corpus
        
    def get_inverted_index(self):
        """
        The method to get the inverted index.

        Returns
        -------
        dictionary
            The inverted index.

        """
        return self.inverted_index
    
    def set_inverted_index(self, inverted_index):
        """
        The method to set the inverted index.

        Parameters
        ----------
        inverted_index : dictionary
            The inverted index.

        Returns
        -------
        None.

        """
        self.inverted_index = inverted_index