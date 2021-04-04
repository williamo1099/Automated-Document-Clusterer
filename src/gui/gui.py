
from gui.frame.MenuBar import MenuBar
from gui.frame.SearchFrame import SearchFrame
from gui.frame.ClusterFrame import ClusterFrame
from gui.frame.ProgressFrame import ProgressFrame

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
        self.__cluster_status = False
        self.__canvas_status = False
        self.__cut_status = False
        self.__folder_path = ''
        self.__corpus = []
        self.__inverted_index = None
        
        # Initialize the application's gui.
        self.__window = tk.Tk()
        self.__window.title('Automated Document Clusterer')
        self.__window.tk.call('wm', 'iconphoto', self.window._w, tk.PhotoImage(file='resources/logo25.png'))
        self.__window.geometry('750x450')
        self.__window.resizable(width=False, height=False)
        self.__window.configure(background='white')
        
        # Initialize the option variables.
        self.__preprocessor_option = [tk.BooleanVar(),
                                    tk.BooleanVar(),
                                    tk.BooleanVar(),
                                    tk.BooleanVar()]
        self.__autorenaming_option = tk.BooleanVar()
        
        # Initialize the menu bar and frames.
        self.__menu_bar = MenuBar(self)
        self.__search_frame = SearchFrame(self)
        self.__cluster_frame = ClusterFrame(self, ['single', 'complete', 'average'])
        self.__progress_frame = ProgressFrame(self)
    
    @property
    def window(self):
        """
        The method to get the main gui window.
        
        Returns
        -------
        Tk Interface
            The main gui window.
            
        """
        return self.__window
    
    @property
    def cluster_status(self):
        """
        The method to get the cluster status.
        Cluster status indicates whether it is ready to do clustering process or not.
        
        Returns
        -------
        boolean
            The cluster status.
        
        """
        return self.__cluster_status
    
    @cluster_status.setter
    def cluster_status(self, cluster_status):
        """
        The method to set the cluster status.
        
        Parameters
        ----------
        cluster_status : boolean
            The cluster status.
        
        Returns
        -------
        None.
        
        """
        self.__cluster_status = cluster_status
    
    @property
    def canvas_status(self):
        """
        The method to get the canvas status.
        Canvas status indicates whether it is ready to draw on canvas or not.
        
        Returns
        -------
        boolean
            The canvas status.
        
        """
        return self.__canvas_status
    
    @canvas_status.setter
    def canvas_status(self, canvas_status):
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
        self.__canvas_status = canvas_status
    
    @property
    def cut_status(self):
        """
        The method to get the cut-off status.
        Cut-off status indicates whether it is ready to cut the dendrogram or not.

        Returns
        -------
        boolean
            The cut-off status.

        """
        return self.__cut_status
    
    @cut_status.setter
    def cut_status(self, cut_status):
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
        self.__cut_status = cut_status
    
    @property
    def folder_path(self):
        """
        The method to get the folder path of corpus.

        Returns
        -------
        string
            The folder path.

        """
        return self.__folder_path
    
    @folder_path.setter
    def folder_path(self, folder_path):
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
        self.__search_frame._set_folder_entry(folder_path)
        self.__folder_path = folder_path
    
    @property
    def corpus(self):
        """
        The method to get corpus.

        Returns
        -------
        list
            The list of documents.

        """
        return self.__corpus
    
    @corpus.setter
    def corpus(self, corpus):
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
        self.__corpus = corpus
    
    @property
    def inverted_index(self):
        """
        The method to get the inverted index.

        Returns
        -------
        dictionary
            The inverted index.

        """
        return self.__inverted_index
    
    @inverted_index.setter
    def inverted_index(self, inverted_index):
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
        self.__inverted_index = inverted_index
    
    @property
    def preprocessor_option(self):
        """
        The method to get the preprocessor option.
        The option is consisting of stop words removal option, stemming option, case folding option and normalization option.

        Returns
        -------
        list
            The preprocessor option.

        """
        return self.__preprocessor_option
    
    @property
    def autorenaming_option(self):
        """
        The method to get the autorenaming option.

        Returns
        -------
        BooleanVar
            The autorenaming option.

        """
        return self.__autorenaming_option
        
    def start(self):
        """
        The method to start application's gui.

        Returns
        -------
        None.

        """
        self.__window.mainloop()
    
    def _restart(self):
        """
        The method to restore application's conditions to original.

        Returns
        -------
        None.

        """
        # Restart all frames contained in window.
        self.__search_frame._restart()
        self.__cluster_frame._restart()
        self.__progress_frame._restart()
        
        # Reinitialize all variables.
        self.__cluster_status = False
        self.__canvas_status = False
        self.__folder_path = ''
        self.__corpus = []
        self.__inverted_index = None
        
        # Set progress bar value to 0.
        self._set_progress_value(0)
    
    def _set_progress_value(self, value):
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
        self.__progress_frame._update_progress_bar(value)
    
    def _set_progress_label(self, second):
        """
        The method to set the progress label text.

        Parameters
        ----------
        second : float
            The time shown on progress label.

        Returns
        -------
        None.

        """
        self.__progress_frame._update_progress_label(second)
    
    def _update_inverted_index(self, extended_corpus):
        """
        The method to update the inverted index.

        Parameters
        ----------
        extended_corpus : list
            The new added documents list.

        Returns
        -------
        None.

        """
        self.__search_frame._update_inverted_index(self.__inverted_index, extended_corpus)