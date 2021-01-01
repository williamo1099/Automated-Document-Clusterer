
import tkinter as tk

class AboutWindow:
    
    def __init__(self, gui):
        """
        The constructor fot AboutWindow class.

        Parameters
        ----------
        gui : gui
            The main gui.

        Returns
        -------
        None.

        """
        self.gui = gui
        
        # Initialize the about window.
        about_window = tk.Toplevel(master=self.gui.get_window())
        about_window.title('About')
        about_window.tk.call('wm', 'iconphoto', about_window._w, tk.PhotoImage(file='resources/logo25.png'))
        about_window.geometry('300x300')
        about_window.resizable(width=False, height=False)
        
        # Initialize the logo in the window.
        app_logo = tk.PhotoImage(file='resources/logo100.png', width=100, height=100)
        panel = tk.Label(master=about_window, image=app_logo)
        panel.pack(side='top', pady=10)
        
        # Initialize the title label in the window.
        title_label = tk.Label(master=about_window, text='Automated Document Clusterer')
        title_label.configure(font=("bold"))
        title_label.pack(side='top', pady=1)
        
        # Initialize the version label in the window.
        version_label = tk.Label(master=about_window, text='Version 0.0.0')
        version_label.pack(side='top', pady=1)
        
        # Initialize the dependency label in the window.
        dependency_label = tk.Label(master=about_window, text='Built with\n' +
                                    'Matplotlib 3.3.2\n' + 'NLTK 3.5\n' + 'SciPy 1.5.4')
        dependency_label.pack(side='top', pady=2)
        
        # Initialize the version label in the window.
        copyright_label = tk.Label(master=about_window, text='Copyright (c) 2020 HotSpace')
        copyright_label.configure(fg='#808080')
        copyright_label.pack(side='bottom', pady=10)
        
        # Start the about window.
        about_window.mainloop()