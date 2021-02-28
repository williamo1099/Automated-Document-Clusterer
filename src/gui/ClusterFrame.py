
from clustering.Clusterer import Clusterer
from gui.NavigationToolbar import NavigationToolbar
from gui.window.FigureWindow import FigureWindow
from gui.WarningPopup import WarningPopup
from gui.ToolTip import ToolTip

import threading
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ClusterFrame:
    
    def __init__(self, gui):
        """
        The constructor for ClusterFrame class.

        Parameters
        ----------
        gui : gui
            The main gui.

        Returns
        -------
        None.

        """
        self.gui = gui
        
        # Initialize the cluster frame in window.
        cluster_frame = tk.Frame(master=self.gui.get_window())
        cluster_frame.pack(side='top')
        cluster_frame.configure(background='white')
        
        # Initialize the method combobox in the frame.
        self.method_list = ['single', 'complete', 'average']
        self.method_combobox = ttk.Combobox(master=self.gui.get_window(), values=self.method_list)
        self.method_combobox.current(0)
        self.method_combobox.pack(in_=cluster_frame, side='left', padx=2, pady=2)
        self.method_combobox.configure(background='white')
        
        # Initialize the cluster button in the frame.
        self.cluster_button = tk.Button(master=self.gui.get_window(), text='Cluster', command=self.cluster)
        self.cluster_button.pack(in_=cluster_frame, side='right', padx=2, pady=2)
        self.cluster_button.configure(background='white')
        ToolTip(self.cluster_button, 'Start clustering all documents')
        
        # Initialize the variable.
        self.clusterer = None
        self.figure = None
    
    def restart(self):
        """
        The method to restore the frame's conditions to original.

        Returns
        -------
        None.

        """
        self.clusterer = None
        if self.gui.get_canvas_status() is True:
            self.reset_canvas()
    
    def cluster(self):
        """
        The method to start clustering documents.

        Returns
        -------
        None.

        """
        # Check whether cluster status is True or not.
        # It is true when it is ready to do clustering.
        if self.gui.get_cluster_status() is True:
            # Start clustering.
            clustering_thread = threading.Thread(target=self.do_clustering, args=(0,), daemon=True, name='clustering_thread')
            clustering_thread.start()
            
            # Draw figure on canvas.
            self.draw_on_canvas()
        else:
            popup = WarningPopup('Clustering process',
                                 'There are no documents to be clustered.')
            popup.show_popup()
    
    def do_clustering(self, cut_off=0):
        """
        The method to do clustering process.

        Parameters
        ----------
        cut_off : float, optional
            The height of a cut-off point. The default is 0.

        Returns
        -------
        None.

        """
        # Start progress bar, with value equals to 0.
        self.gui.set_progress_value(0)        
        self.clusterer = Clusterer(self.gui.get_corpus())
        self.gui.set_progress_value(5)
        
        # Start the clustering process.
        self.clusterer.cluster(self.method_list[self.method_combobox.current()], cut_off)
        self.gui.set_progress_value(90)
        
        # Set the figure get from clustering process.
        # Calculate proper figure size based on corpus size.
        figsize = [10, 5]
        if len(self.gui.get_corpus()) > 50:
            figsize = [10, 5]
        self.figure = self.clusterer.get_dendrogram(figsize)
        self.gui.set_progress_value(100)
    
    def draw_on_canvas(self):
        """
        The method to draw the dendrogram figure on canvas.

        Returns
        -------
        None.

        """
        # Reset the canvas if it has been drawn.
        self.reset_canvas()
        
        if self.figure is not None and self.clusterer is not None:
            # Set canvas status to True.
            self.gui.set_canvas_status(True)
            
            def canvas_on_click(event):
                """
                The method to handle on click event on canvas.
    
                Parameters
                ----------
                event : Event
                    An event indicating a click from user.
    
                Returns
                -------
                None.
    
                """
                # Check whether cut status is True or not.
                if event.inaxes is not None and self.gui.get_cut_status() is True:
                    cut_off = event.xdata
                    self.reset_canvas()
                    
                    # Start clustering.
                    clustering_thread = threading.Thread(target=self.do_clustering, args=(cut_off,), daemon=True, name='clustering_thread')
                    clustering_thread.start()
                    
                    # Draw figure on canvas.
                    self.draw_on_canvas()
            
            # Check the corpus size.
            # If the size is more than 50, the figure will be displayed in a separated window.
            if len(self.gui.get_corpus()) <= 50:
                # Draw figure on canvas.
                self.figure_canvas = FigureCanvasTkAgg(self.figure, master=self.gui.get_window())
                self.figure_canvas.draw()
                self.figure_canvas.callbacks.connect('button_press_event', canvas_on_click)
                
                # Add canvas toolbar.
                self.figure_toolbar = NavigationToolbar(self.figure_canvas, self.gui, self.clusterer)
                self.figure_canvas.get_tk_widget().pack(pady=2)
            else:
                # Initialize info label.
                self.info_label = ttk.Label(self.gui.get_window(), text='Figure is displayed in a separated window.')
                self.info_label.configure(background='white')
                self.info_label.pack(pady=2)
                
                # Initialize figure window.
                self.figure_window = FigureWindow(self.gui, self.clusterer, self.figure, canvas_on_click)
                self.figure_window.start()
        else:
            self.gui.get_window().after(500, self.draw_on_canvas)
    
    def reset_canvas(self):
        """
        The method to reset the figure, drawn canvas and result frame.

        Returns
        -------
        None.

        """
        # Check whether canvas status is True or not.
        # It is true when a figure has been drawn on canvas.
        if self.gui.get_canvas_status() is True:
            self.figure = None
            
            # Check the corpus size.
            # If the size is more than 50, the figure is displayed in a separated window.
            if len(self.gui.get_corpus()) <= 50:
                self.figure_canvas.get_tk_widget().destroy()
                self.figure_toolbar.destroy()
            else:
                self.info_label.destroy()
                self.figure_window.reset()
            
            self.gui.set_canvas_status(False)