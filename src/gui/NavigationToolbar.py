
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import os
import shutil

class NavigationToolbar(NavigationToolbar2Tk):
    
    def __init__(self, figure_canvas, gui, cluster_list):
        self.gui = gui
        self.toolitems = (
            ('Home', 'Reset original view', 'home', 'home'),
            ('Back', 'Back to previous view', 'back', 'back'),
            ('Forward', 'Forward to next view', 'forward', 'forward'),
            ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
            ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
            ('Subplots', 'Configure subplots', 'subplots', 'configure_subplots'),
            ('Organize', 'Organize the documents', 'home', 'organize_documents'),
            ('Save', 'Save the figure', 'filesave', 'save_figure'),
        )
        NavigationToolbar2Tk.__init__(self, figure_canvas, self.gui.get_window())
        
        self.cluster_list = cluster_list
        
    def organize_documents(self):
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
        self.push_current()
        
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