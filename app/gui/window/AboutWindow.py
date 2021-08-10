
import tkinter as tk

class AboutWindow:
    
    def __init__(self, gui):
        """
        The constructor for AboutWindow class.

        Parameters
        ----------
        gui : gui
            The main gui.
        clusterer : Clusterer
            The clusterer which did the clustering process.

        Returns
        -------
        None.

        """
        self.__gui = gui
        
        # Initialize the about window.
        self.__window = tk.Toplevel(master=self.__gui.window)
        self.__window.title('About')
        self.__window.tk.call('wm', 'iconphoto', self.__window._w, tk.PhotoImage(file='resources/logo25.png'))
        self.__window.geometry('300x300')
        self.__window.resizable(width=False, height=False)
        
        # Initialize the logo in the window.
        self.__app_logo = tk.PhotoImage(file='resources/logo100.png', width=100, height=100)
        self.__panel = tk.Label(master=self.__window, image=self.__app_logo)
        self.__panel.pack(side='top', pady=10)
        
        # Initialize the title label in the window.
        self.__title_label = tk.Label(master=self.__window, text='Automated Document Clusterer')
        self.__title_label.configure(font=("bold"))
        self.__title_label.pack(side='top', pady=1)
        
        # Initialize the version label in the window.
        self.__version_label = tk.Label(master=self.__window, text='Version 0.0.0')
        self.__version_label.pack(side='top', pady=1)
        
        # Initialize the dependency label in the window.
        self.__dependency_label = tk.Label(master=self.__window, text='Built with\n' +
                                    'Matplotlib 3.3.2\n' + 'NLTK 3.5\n' + 'SciPy 1.5.4')
        self.__dependency_label.pack(side='top', pady=2)
        
        # Initialize the version label in the window.
        self.__copyright_label = tk.Label(master=self.__window, text='Copyright (c) 2020')
        self.__copyright_label.configure(fg='#808080')
        self.__copyright_label.pack(side='bottom', pady=10)
    
    def _start(self):
        """
        The method to start the about window.

        Returns
        -------
        None.

        """
        self.__window.mainloop()