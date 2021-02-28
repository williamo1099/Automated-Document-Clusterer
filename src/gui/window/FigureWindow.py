
from gui.NavigationToolbar import NavigationToolbar

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class FigureWindow:
    
    def __init__(self, gui, clusterer, figure, on_click):
        """
        The constructor for FigureWindow class.

        Parameters
        ----------
        gui : gui
            The main gui.
        figure : figure
            The dendrogram figure.

        Returns
        -------
        None.

        """
        self.gui = gui
        
        # Initialize the figure window.
        self.window = tk.Toplevel(master=self.gui.get_window())
        self.window.title('Figure')
        
        # Draw figure on canvas.
        self.figure_canvas = FigureCanvasTkAgg(figure, master=self.window)
        self.figure_canvas.draw()
        self.figure_canvas.callbacks.connect('button_press_event', on_click)
        
        # Add canvas toolbar.
        self.figure_toolbar = NavigationToolbar(self.figure_canvas, self.gui, clusterer)
        self.figure_canvas.get_tk_widget().pack(pady=2)
    
    def start(self):
        """
        The method to start the figure window.

        Returns
        -------
        None.

        """
        self.window.mainloop()
    
    def reset(self):
        """
        The method to reset the figure window.

        Returns
        -------
        None.

        """
        self.figure_canvas.get_tk_widget().destroy()
        self.figure_toolbar.destroy()
        self.window.destroy()