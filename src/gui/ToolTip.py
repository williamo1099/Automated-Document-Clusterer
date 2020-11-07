
import tkinter as tk

class ToolTip:
    
    def __init__(self, widget, tip):
        self.widget = widget
        self.widget.bind('<Enter>', self.enter)
        self.widget.bind('<Leave>', self.close)
        self.tip = tip
        
    def enter(self, event=None):
        """
        Method untuk menampilkan tool tip ketika mouse mendekati widget.

        Parameters
        ----------
        event : Event, optional
            Deskripsi event. Nilai default adalah None.

        Returns
        -------
        None.

        """
        x = y = 0
        x, y, cx, cy = self.widget.bbox('insert')
        x += self.widget.winfo_rootx() + 30
        y += self.widget.winfo_rooty() + 20
        
        self.tool_tip = tk.Toplevel(self.widget)
        self.tool_tip.wm_overrideredirect(True)
        self.tool_tip.wm_geometry('+%d+%d' % (x, y))
        label = tk.Label(self.tool_tip,
                         text=self.tip)
        label.pack(ipadx=5)
        
    def close(self, event=None):
        """
        Method untuk menghilangkan tool tip ketika mouse menjauhi widget.

        Parameters
        ----------
        event : Event, optional
            Deskripsi event. Nilai default adalah None.

        Returns
        -------
        None.

        """
        if self.tool_tip:
            self.tool_tip.destroy()