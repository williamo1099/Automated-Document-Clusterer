
from gui.window.WarningPopup import WarningPopup
from gui.ToolTip import ToolTip

import os
import shutil
import tkinter as tk
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

class NavigationToolbar(NavigationToolbar2Tk):
    
    def __init__(self, figure_canvas, gui, clusterer):
        """
        The constructor for NavigationToolbar class.

        Parameters
        ----------
        figure_canvas : FigureCanvas
            Canvas on which figure is drawn.
        gui : gui
            The main gui.
        clusterer : Clusterer
            The clusterer which did the clustering process.

        Returns
        -------
        None.

        """
        self.__gui = gui
        self.__clusterer = clusterer
        NavigationToolbar2Tk.__init__(self, figure_canvas, self.__gui.window)
        
        # Initialize the cut button.
        self.__cut_icon = tk.PhotoImage(file='resources/icon/cut.png', width=25, height=25)
        self.__cut_button = tk.Button(master=self, image=self.__cut_icon, command=self.__cut_dendrogram, relief='sunken' if self.__gui.cut_status else 'raised')
        self.__cut_button.pack(side='left')
        ToolTip(self.__cut_button, 'Cut the dendrogram')
        
        # Initialize the organize button.
        self.__organize_icon = tk.PhotoImage(file='resources/icon/organize.png', width=25, height=25)
        self.__organize_button = tk.Button(master=self, image=self.__organize_icon, command=self.__organize_documents)
        self.__organize_button.pack(side='left')
        ToolTip(self.__organize_button, 'Organize all documents')
        
        # Initialize the evaluate button.
        self.__evaluate_icon = tk.PhotoImage(file='resources/icon/evaluate.png', width=25, height=25)
        self.__evaluate_button = tk.Button(master=self, image=self.__evaluate_icon, command=self.__evaluate_result)
        self.__evaluate_button.pack(side='left')
        ToolTip(self.__evaluate_button, 'Evaluate clustering result')
        
    def __cut_dendrogram(self):
        """
        The method to set the cut status to true, indicating it is ready to cut the dendrogram, or false.

        Returns
        -------
        None.

        """
        self.__gui.cut_status = (not self.__gui.cut_status)
        
        # Change the button appearance to indicate if cut status is on or off.
        if self.__gui.cut_status:
            self.__cut_button.config(relief='sunken')
        else:
            self.__cut_button.config(relief='raised')
        
    def __organize_documents(self):
        """
        The method to organize documents into folders based on documents' clusters.
        Currently this feature is only compatible with Windows file system.

        Returns
        -------
        None.

        """
        # Get cluster list.
        cluster_list = self.__clusterer.extract_clusters(sorted(list(self.__gui.inverted_index.keys()), key=str.lower), self.__gui.autorenaming_option.get())
        
        # Create a new folder organized.
        folder = 'organized'
        organized_folder = os.path.join(self.__gui.folder_path, folder)
        if not os.path.exists(organized_folder):
            os.mkdir(organized_folder)
            
            # For each label, put all documents together in the same folder.
            for cluster, doc in cluster_list.items():
                # Create a new folder for current cluster.
                ci_folder = os.path.join(organized_folder, cluster)
                os.mkdir(ci_folder)
                for item in doc:
                    # Copy and move the document into the cluster folder.
                    source = os.path.join(self.__gui.folder_path, item + '.txt')
                    shutil.copyfile(source, ci_folder + '/' + item + '.txt')
        else:
            # If the organized folder exists, a warning popup will show up.
            popup = WarningPopup(self.__gui, 'Organizing files',
                                  'Folder exists.')
            popup._start()
    
    def __evaluate_result(self):
        """
        The method to evaluate cluster result.
        Evaluation done is internal evaluation (using cophenetic correlation coefficient).

        Returns
        -------
        None

        """
        # Evaluate internally using cophenetic correlation coefficient.
        cpcc = self.__clusterer.calc_cophenetic_coeff()
        
        # Show evaluation through a popup window.
        popup = WarningPopup(self.__gui, 'Clustering evaluation',
                              'Cophenetic correlation coefficient : ' + str(cpcc))
        popup._start()