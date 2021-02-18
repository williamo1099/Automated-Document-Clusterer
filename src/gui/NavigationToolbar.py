
from gui.ToolTip import ToolTip

import os
import shutil
import tkinter as tk
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk

class NavigationToolbar(NavigationToolbar2Tk):
    
    def __init__(self, figure_canvas, gui, cluster_list):
        self.gui = gui
        self.cluster_list = cluster_list
        
        NavigationToolbar2Tk.__init__(self, figure_canvas, self.gui.get_window())
        
        # Initialize the cut button.
        self.cut_icon = tk.PhotoImage(file='resources/Icons/cut.png', width=25, height=25)
        self.cut_button = tk.Button(master=self, image=self.cut_icon, command=self.cut_dendrogram)
        self.cut_button.pack(side='left')
        ToolTip(self.cut_button, 'Cut the dendrogram')
        
        # Initialize the organize button.
        self.organize_icon = tk.PhotoImage(file='resources/Icons/organize.png', width=25, height=25)
        self.organize_button = tk.Button(master=self, image=self.organize_icon, command=self.organize_documents)
        self.organize_button.pack(side='left')
        ToolTip(self.organize_button, 'Organize all documents')
        
    def cut_dendrogram(self):
        """
        The method to set the cut status to true, indicating it is ready to cut the dendrogram.

        Returns
        -------
        None.

        """
        self.gui.set_cut_status(not self.gui.get_cut_status())
        
    def organize_documents(self):
        """
        The method to organize documents into folders based on documents' clusters.
        Currently this feature is only compatible with MacOS file system.

        Returns
        -------
        None.

        """
        # Create a new folder organized.
        folder = 'organized'
        organized_folder = os.path.join(self.gui.get_folder_path(), folder)
        if not os.path.exists(organized_folder):
            os.mkdir(organized_folder)
            
        # For each label, put all documents together in the same folder.
        for cluster, doc in self.cluster_list.items():
            
            # Create a new folder for current cluster.
            ci_folder = os.path.join(organized_folder, cluster)
            os.mkdir(ci_folder)
            for item in doc:
                
                # Copy and move the document into the cluster folder.
                source = os.path.join(self.gui.get_folder_path(), item + '.txt')
                shutil.copyfile(source, ci_folder + '/' + item + '.txt')
        else:
            print('File exists')