
import tkinter as tk
from tkinter import ttk

class ProgressFrame:
    
    def __init__(self, gui):
        """
        The constructor for ProgressFrame class.

        Parameters
        ----------
        gui : gui
            The main gui.

        Returns
        -------
        None.

        """
        self.__gui = gui
        
        # Initialize the progress frame in window.
        frame = tk.Frame(master=self.__gui.window)
        frame.pack(side='bottom', fill='x')
        frame.configure(background='white')
        
        # Initialize the progress bar in the frame.
        self.__progress_bar = ttk.Progressbar(master=self.__gui.window, orient='horizontal')
        self.__progress_bar.pack(in_=frame, fill='x', padx=2, pady=2)
        
    def _update_progress_bar(self, value):
        """
        The method to update the progress bar value.

        Parameters
        ----------
        value : int
            The progress bar value, in range of 0 and 100.

        Returns
        -------
        None.

        """
        if value >= 0 & value <= 100:
            self.__progress_bar['value'] = value