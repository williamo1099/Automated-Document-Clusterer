
import tkinter as tk

class WarningPopup:
    
    def __init__(self, gui, popup_title, warning_message):
        """
        The constructor for WarningPopup class.

        Parameters
        ----------
        gui : gui
            The main gui.
        popup_title : string
            The popup title.
        warning_message : string
            The popup message.

        Returns
        -------
        None.

        """
        self.__gui = gui
        
        # Initialize the warning popup window.
        self.__window = tk.Toplevel(master=self.__gui.window)
        self.__window.title(warning_message)
        
        # Initialize the warning label.
        self.__warning_label = tk.Label(self.__window, text=warning_message)
        self.__warning_label.pack(side='top',
                   fill='x',
                   pady=10,
                   padx=5)
        
        # Initialize the OK button.
        self.__ok_button = tk.Button(self.__window,
                              text='Ok',
                              command=self.__window.destroy)
        self.__ok_button.pack()
    
    def _start(self):
        """
        The method to start the warning popup window.

        Returns
        -------
        None.

        """
        self.__window.mainloop()