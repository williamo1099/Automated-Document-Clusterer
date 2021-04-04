
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
        self.__progress_bar.pack(in_=frame, side='left', fill='x', expand='yes', padx=2, pady=2)
        
        # Initialize the progress label in the frame.
        self.__progress_label = ttk.Label(master=self.__gui.window, text='0 second')
        self.__progress_label.configure(background='white')
        self.__progress_label.pack(in_=frame, side='right', fill='x', padx=2, pady=2)
    
    def _restart(self):
        """
        The method to restore the frame's conditions to original.

        Returns
        -------
        None.

        """
        self._update_progress_bar(0)
        self._update_progress_label(0)
        
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
            
    def _update_progress_label(self, second):
        """
        The method to update the progress label text.

        Parameters
        ----------
        second : float
            The time (in second) shown on progress label.

        Returns
        -------
        None.

        """
        time = round(second, 2)
        self.__progress_label.config(text=str(time) + (' seconds' if time > 0 else ' second'))