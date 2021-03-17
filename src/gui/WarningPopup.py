
import tkinter as tk

class WarningPopup:
    
    def __init__(self, popup_title, warning_message):
        """
        The constructor for WarningPopup class.

        Parameters
        ----------
        popup_title : string
            The popup title.
        warning_message : string
            The popup message.

        Returns
        -------
        None.

        """
        self.__popup_title = popup_title
        self.__warning_message = warning_message
        
    def _show_popup(self):
        """
        The method to show popup warning.
        
        Returns
        -------
        None.

        """
        warning_popup = tk.Tk()
        warning_popup.wm_title(self.__popup_title)
        label = tk.Label(warning_popup,
                         text=self.__warning_message)
        label.pack(side='top',
                   fill='x',
                   pady=10,
                   padx=5)
        
        # Initialize the OK button.
        ok_button = tk.Button(warning_popup,
                              text='Ok',
                              command=warning_popup.destroy)
        ok_button.pack()
        warning_popup.mainloop()