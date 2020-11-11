
import tkinter as tk

class WarningPopup:
    
    def __init__(self, popup_title, warning_message):
        self.popup_title = popup_title
        self.warning_message = warning_message
        
    def show_popup(self):
        """
        Method untuk menampilkan pop-up warning.
        
        Returns
        -------
        None.

        """
        warning_popup = tk.Tk()
        warning_popup.wm_title(self.popup_title)
        label = tk.Label(warning_popup,
                         text=self.warning_message)
        label.pack(side='top',
                   fill='x',
                   pady=10,
                   padx=5)
        ok_button = tk.Button(warning_popup,
                              text='Ok',
                              command=warning_popup.destroy)
        ok_button.pack()
        warning_popup.mainloop()