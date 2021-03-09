
from gui.WarningPopup import WarningPopup
from gui.ToolTip import ToolTip

import os
import shutil
import tkinter as tk
from tkinter import filedialog
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
        self.gui = gui
        self.clusterer = clusterer
        
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
        
        # Initialize the evaluate button.
        self.evaluate_icon = tk.PhotoImage(file='resources/Icons/evaluate.png', width=25, height=25)
        self.evaluate_button = tk.Button(master=self, image=self.evaluate_icon, command=self.evaluate_result)
        self.evaluate_button.pack(side='left')
        ToolTip(self.evaluate_button, 'Evaluate clustering result')
        
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
        Currently this feature is only compatible with Windows file system.

        Returns
        -------
        None.

        """
        # Get cluster list.
        cluster_list = self.clusterer.extract_clusters(sorted(list(self.gui.get_inverted_index().keys()), key=str.lower), self.gui.get_autorenaming_option().get())
        
        # Create a new folder organized.
        folder = 'organized'
        organized_folder = os.path.join(self.gui.get_folder_path(), folder)
        if not os.path.exists(organized_folder):
            os.mkdir(organized_folder)
            
        # For each label, put all documents together in the same folder.
        for cluster, doc in cluster_list.items():
            # Create a new folder for current cluster.
            ci_folder = os.path.join(organized_folder, cluster)
            os.mkdir(ci_folder)
            for item in doc:
                
                # Copy and move the document into the cluster folder.
                source = os.path.join(self.gui.get_folder_path(), item + '.txt')
                shutil.copyfile(source, ci_folder + '/' + item + '.txt')
        else:
            # If the organized folder exists, a warning popup will show up.
            popup = WarningPopup('Organizing files',
                                  'Folder exists.')
            popup.show_popup()
    
    def evaluate_result(self):
        """
        The method to evaluate cluster result.
        Evaluation done is internal evaluation (using cophenetic correlation coefficient) and external evaluation (using F-score).

        Returns
        -------
        None

        """
        # Evaluate internally using cophenetic correlation coefficient.
        cpcc = self.clusterer.calc_cophenetic_coeff()
        
        # Evaluate externally using F-measure.
        folder_path = filedialog.askdirectory()
        print(folder_path)
        if folder_path != '':
            doc_titles = []
            for root, directories, files in os.walk(folder_path):
                for file in files:
                    if '.txt' in file:
                        doc_titles.append(os.path.join(root, file))
            
            escaped_folder_path = str(folder_path) + '\\'
        
            # Get benchmark data.
            benchmark = {}
            for i in range(0, len(doc_titles)):
                doc_title = os.path.splitext(doc_titles[i])[0].replace(escaped_folder_path, '')
                cluster = doc_title.split('\\')[0]
                title = doc_title.split('\\')[1]
                
                if cluster not in benchmark:
                    benchmark[cluster] = []
                benchmark[cluster].append(title)
            f_score = self.clusterer.calc_f_score(benchmark)
        
            # Show evaluation through a popup window.
            popup = WarningPopup('Clustering evaluation',
                                 'Cophenetic correlation coefficient : ' + str(cpcc) + '\n' +
                                 'F-score : ' + str(f_score))
            popup.show_popup()
        else:
            # This means that user does not provide benchmark data.
            # Show evaluation through a popup window.
            popup = WarningPopup('Clustering evaluation',
                                  'Cophenetic correlation coefficient : ' + str(cpcc) + '\n' +
                                  'F-score : -')
            popup.show_popup()