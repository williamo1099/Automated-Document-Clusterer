
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
        self.gui = gui
        
        # Initialize the progress frame in window.
        progress_frame = tk.Frame(master=self.gui.get_window())
        progress_frame.pack(side='bottom', fill='x')
        progress_frame.configure(background='white')
        
        # Initialize the progress bar in the frame.
        self.progress_bar = ttk.Progressbar(master=self.gui.get_window(), orient='horizontal')
        self.progress_bar.pack(in_=progress_frame, fill='x', padx=2, pady=2)
        
        # Initialize the progress info label in the frame.
        # self.progress_info_text = tk.StringVar()
        # self.progress_info_text.set('None')
        # self.progress_info = tk.Label(master=self.gui.get_window(), textvariable=self.progress_info_text)
        # self.progress_info.pack(in_=progress_frame, side='right', padx=2, pady=2)
        
    def update_progress_bar(self, value):
        """
        The method to update the progress bar value.

        Parameters
        ----------
        value : int
            The progress bar value.

        Returns
        -------
        None.

        """
        self.progress_bar['value'] = value