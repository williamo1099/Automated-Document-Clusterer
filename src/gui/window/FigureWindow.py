
from gui.frame.NavigationToolbar import NavigationToolbar

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class FigureWindow:
    
    def __init__(self, gui, clusterer, figure, canvas_on_click):
        """
        The constructor for FigureWindow class.

        Parameters
        ----------
        gui : gui
            The main gui.
        clusterer : Clusterer
            The clusterer which did the clustering process.
        figure : figure
            The dendrogram figure.
        canvas_on_click : function
            The on click function.

        Returns
        -------
        None.

        """
        self.__gui = gui
        
        # Initialize the figure window.
        self.__window = tk.Toplevel(master=self.__gui.window)
        self.__window.title('Figure')
        
        # Draw figure on canvas.
        self.__figure_canvas = FigureCanvasTkAgg(figure, master=self.window)
        self.__figure_canvas.draw()
        self.__figure_canvas.callbacks.connect('button_press_event', canvas_on_click)
        
        # Add canvas toolbar.
        self.__figure_toolbar = NavigationToolbar(self.__figure_canvas, self.__gui, clusterer)
        self.__figure_canvas.get_tk_widget().pack(pady=2)
    
    def _start(self):
        """
        The method to start the figure window.

        Returns
        -------
        None.

        """
        self.__window.mainloop()
    
    def _reset(self):
        """
        The method to reset the figure window.

        Returns
        -------
        None.

        """
        self.__figure_canvas.get_tk_widget().destroy()
        self.__figure_toolbar.destroy()
        self.__window.destroy()