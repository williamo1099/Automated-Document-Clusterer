
from gui.ToolTip import ToolTip

import tkinter as tk
from tkinter import filedialog
import os
import shutil

class ResultFrame:
    
    def __init__(self, gui, cluster_list, figure):
        """
        The constructor for ResultFrame class.

        Parameters
        ----------
        gui : gui
            The main gui.

        Returns
        -------
        None.

        """
        self.gui = gui
        
        # Initialize the result frame in window.
        result_frame = tk.Frame(self.gui.get_window())
        result_frame.pack(side='top')
        result_frame.configure(background='white')
        
        # Initialize the organize button in the frame.
        self.organize_button = tk.Button(master=self.gui.get_window(), text='Organize documents',
                                         command=lambda:self.organize_document(cluster_list))
        self.organize_button.pack(in_=result_frame, side='left', padx=5, pady=5)
        self.organize_button.configure(background='white')
        ToolTip(self.organize_button, 'Organize document files based on the dendrogram')
        
        # Initialize the download button in the frame.
        self.download_button = tk.Button(master=self.gui.get_window(), text='Download plot',
                                    command=lambda:self.save_plot(figure))
        self.download_button.pack(in_=result_frame, side='right', padx=5, pady=5)
        self.download_button.configure(background='white')
        ToolTip(self.download_button, 'Download the plot')
       
    def restart(self):
        """
        The method to restore the frame's conditions to original.

        Returns
        -------
        None.

        """
        self.organize_button.destroy()
        self.download_button.destroy()
    
    def organize_document(self, cluster_list):
        """
        The method to organize documents into folders based on documents' clusters.
        Currently this feature is only compatible with MacOS file system.

        Parameters
        ----------
        cluster_list : dictionary
            The list of objects of each clusters.
            Written as {cluster1: [doc1, doc2], cluster2: [doc3], etc.}.

        Returns
        -------
        None.

        """
        # Create a new folder organized.
        folder = 'organized'
        organized_folder = os.path.join(self.gui.get_folder_path(), folder)
        if not os.path.exists(organized_folder):
            os.mkdir(organized_folder)
            
        # .For each label, put all documents together in the same folder.
        for cluster, doc in cluster_list.items():
            
            # Create a new folder for current cluster.
            ci_folder = os.path.join(organized_folder, cluster)
            os.mkdir(ci_folder)
            for item in doc:
                
                # Copy and move the document into the cluster folder.
                source = os.path.join(self.gui.get_folder_path(), item + '.txt')
                shutil.copyfile(source, ci_folder + '/' + item + '.txt')
        
    def save_plot(self, figure):
        """
        The method to save the dendrogram plot.

        Parameters
        ----------
        figure : Figure
            The dendrogram plot.

        Returns
        -------
        None.

        """
        figure_path = filedialog.asksaveasfilename(defaultextension='.png', filetypes=(('PNG Image', '*.png'),))
        figure.savefig(figure_path)