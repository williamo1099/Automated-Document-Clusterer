
from clustering.Clusterer import Clusterer
from gui.frame.NavigationToolbar import NavigationToolbar
from gui.window.FigureWindow import FigureWindow
from gui.window.WarningPopup import WarningPopup
from gui.ToolTip import ToolTip

import threading
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ClusterFrame:
    
    def __init__(self, gui, method_list):
        """
        The constructor for ClusterFrame class.

        Parameters
        ----------
        gui : gui
            The main gui.
        method_list : list
            The list of all available methods.

        Returns
        -------
        None.

        """
        self.__gui = gui
        
        # Initialize the cluster frame in window.
        frame = tk.Frame(master=self.__gui.window)
        frame.pack(side='top')
        frame.configure(background='white')
        
        # Initialize the method combobox in the frame.
        self.__method_list = method_list
        self.__method_combobox = ttk.Combobox(master=self.__gui.window, values=self.__method_list)
        self.__method_combobox.current(0)
        self.__method_combobox.pack(in_=frame, side='left', padx=2, pady=2)
        self.__method_combobox.configure(background='white')
        
        # Initialize the cluster button in the frame.
        self.__cluster_button = tk.Button(master=self.__gui.window, text='Cluster', command=self.__cluster)
        self.__cluster_button.pack(in_=frame, side='right', padx=2, pady=2)
        self.__cluster_button.configure(background='white')
        ToolTip(self.__cluster_button, 'Start clustering all documents')
        
        # Initialize the variable.
        self.__clusterer = None
        self.__figure = None
    
    def _restart(self):
        """
        The method to restore the frame's conditions to original.

        Returns
        -------
        None.

        """
        self.__clusterer = None
        if self.__gui.canvas_status is True:
            self.__reset_canvas()
    
    def __reset_canvas(self):
        """
        The method to reset the figure, drawn canvas and result frame.

        Returns
        -------
        None.

        """
        # Check whether canvas status is True or not.
        # It is true when a figure has been drawn on canvas.
        if self.__gui.canvas_status is True:
            self.__figure = None
            
            # Check whether the figure is drawn on figure window or not.
            if not self.__drawn_on_figure_window():
                self.__figure_canvas.get_tk_widget().destroy()
                self.__figure_toolbar.destroy()
            else:
                self.__info_label.destroy()
                self.__figure_window._reset()
            self.__gui.canvas_status = False
    
    def __cluster(self):
        """
        The method to start clustering documents.

        Returns
        -------
        None.

        """
        # Check whether cluster status is True or not.
        # It is true when it is ready to do clustering.
        if self.__gui.cluster_status is True:
            # Start clustering.
            clustering_thread = threading.Thread(target=self.__do_clustering, args=(0,True), name='clustering_thread')
            clustering_thread.start()
            
            # Draw figure on canvas.
            self.__draw_on_canvas()
        else:
            popup = WarningPopup(self.__gui, 'Clustering process',
                                 'There are no documents to be clustered.')
            popup._start()
    
    def __do_clustering(self, cut_off=0, restart=True):
        """
        The method to do clustering process.

        Parameters
        ----------
        cut_off : float, optional
            The height of a cut-off point. The default is 0.
        restart : boolean, optional
            The status indicating whether clustering process uses different method. The default is True.

        Returns
        -------
        None.

        """
        # Start the timer.
        start_time = datetime.now()
        
        # Start progress bar, with value equals to 0.
        self.__gui._set_progress_value(0)
        self.__clusterer = Clusterer(self.__gui.corpus) if restart is True else self.__clusterer
        self.__gui._set_progress_value(5)
        
        # Start the clustering process.
        if restart is True:
            self.__clusterer.cluster(self.__method_list[self.__method_combobox.current()])
        self.__gui._set_progress_value(90)
        
        # Finish the timer.
        finish_time = datetime.now() - start_time
        
        # Set the figure get from clustering process.
        # Calculate proper figure size based on corpus size.
        figsize = (10, 5)
        orientation = 'right'
        if self.__drawn_on_figure_window():
            figsize = (20, 10)
            orientation = 'top'
        self.__figure = self.__clusterer.plot_dendrogram(cut_off, figsize, orientation)
        self.__gui._set_progress_value(100)
        
        # Set progress label text.
        self.__gui._set_progress_label(finish_time.total_seconds())
    
    def __draw_on_canvas(self):
        """
        The method to draw the dendrogram figure on canvas.

        Returns
        -------
        None.

        """
        # Reset the canvas if it has been drawn.
        self.__reset_canvas()
        
        if self.__figure is not None and self.__clusterer is not None:
            # Set canvas status to True.
            self.__gui.canvas_status = True
            
            def _canvas_on_click(event):
                # Check whether cut status is True or not.
                if event.inaxes is not None and self.__gui.cut_status is True:
                    if not self.__drawn_on_figure_window():
                        cut_off = event.xdata
                    else:
                        cut_off = event.ydata
                    self.__reset_canvas()
                    
                    # Start clustering.
                    clustering_thread = threading.Thread(target=self.__do_clustering, args=(cut_off,False), name='clustering_thread')
                    clustering_thread.start()
                    
                    # Draw figure on canvas.
                    self.__draw_on_canvas()
            
            # Check whether the figure is drawn on figure window or not.
            if not self.__drawn_on_figure_window():
                # Draw figure on canvas.
                self.__figure_canvas = FigureCanvasTkAgg(self.__figure, master=self.__gui.window)
                self.__figure_canvas.draw()
                self.__figure_canvas.callbacks.connect('button_press_event', _canvas_on_click)
                
                # Add canvas toolbar.
                self.__figure_toolbar = NavigationToolbar(self.__figure_canvas, self.__gui, self.__clusterer)
                self.__figure_canvas.get_tk_widget().pack(pady=2)
            else:
                # Initialize info label.
                self.__info_label = ttk.Label(self.__gui.window, text='Figure is displayed in a separated window.')
                self.__info_label.configure(background='white')
                self.__info_label.pack(pady=2)
                
                # Initialize figure window.
                self.__figure_window = FigureWindow(self.__gui, self.__clusterer, self.__figure, _canvas_on_click)
                self.__figure_window._start()
        else:
            self.__gui.window.after(500, self.__draw_on_canvas)
        
    def __drawn_on_figure_window(self):
        """
        The method to check whether the figure is drawn on figure window or not.

        Returns
        -------
        boolean
            True if the figure is drawn on figure window.

        """
        return len(self.__gui.corpus) > 40