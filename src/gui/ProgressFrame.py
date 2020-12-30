
import tkinter as tk
from tkinter import ttk

class ProgressFrame:
    
    def __init__(self, gui):
        self.gui = gui
        
        # Initialize the progress frame in window.
        progress_frame = tk.Frame(master=self.gui.get_window())
        progress_frame.pack(side='bottom', fill='x')
        progress_frame.configure(background='white')
        
        # Initialize the progress bar in the frame.
        self.progress_bar = ttk.Progressbar(master=self.gui.get_window(), orient='horizontal', length=100)
        self.progress_bar.pack(in_=progress_frame, padx=2, pady=2)