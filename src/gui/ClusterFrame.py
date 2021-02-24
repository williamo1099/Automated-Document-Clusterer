
from clustering.Clusterer import Clusterer
from gui.NavigationToolbar import NavigationToolbar
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
    
    def restart(self):
        """
        The method to restore the frame's conditions to original.

        Returns
        -------
        None.

        """
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
            self.draw_canvas(0)
            # threading.Thread(target=self.draw_canvas, args=(0,), name='drawing_thread').start()
        else:
            popup = WarningPopup('Clustering process',
                                 'There are no documents to be clustered.')
            popup.show_popup()
    
    def draw_canvas(self, cut_off=0):
        """
        The method to draw the dendrogram figure on canvas.

        Parameters
        ----------
        cut_off : float, optional
            The height of a cut-off point. The default is 0.

        Returns
        -------
        None.

        """
        clusterer = Clusterer(self.gui.get_corpus())
        figure = clusterer.cluster(self.method_list[self.method_combobox.current()], cut_off)
        
        # Check whether canvas status is True or not.
        # It is true when a figure has been drawn on canvas.
        if self.gui.get_canvas_status() is True:
            self.reset_canvas()
        else:
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
                self.draw_canvas(cut_off)
        
        # Draw figure on canvas.
        self.figure_canvas = FigureCanvasTkAgg(figure, master=self.gui.get_window())
        self.figure_canvas.draw()
        self.figure_canvas.callbacks.connect('button_press_event', canvas_on_click)
        
        # Add canvas toolbar.
        self.figure_toolbar = NavigationToolbar(self.figure_canvas, self.gui, clusterer)
        self.figure_canvas.get_tk_widget().pack(pady=2)
    
    def reset_canvas(self):
        """
        The method to reset the drawn canvas and result frame.

        Returns
        -------
        None.

        """
        self.cpcc_label.destroy()
        self.figure_canvas.get_tk_widget().destroy()
        self.figure_toolbar.destroy()