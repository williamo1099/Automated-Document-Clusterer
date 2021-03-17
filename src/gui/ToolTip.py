
import tkinter as tk

class ToolTip:
    
    def __init__(self, widget, tip):
        """
        The constructor for ToolTip class.

        Parameters
        ----------
        widget : Tk button
            The button.
        tip : string
            The tool tip message.

        Returns
        -------
        None.

        """
        self.widget = widget
        self.widget.bind('<Enter>', self.__enter)
        self.widget.bind('<Leave>', self.__close)
        self.tip = tip
        
    def __enter(self, event=None):
        """
        The method to show a tooltip when a mouse is hovering the object.

        Parameters
        ----------
        event : Event, optional
            The event indicating a hover. The default is None.

        Returns
        -------
        None.

        """
        x = y = 0
        x, y, cx, cy = self.widget.bbox('insert')
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() - 2
        
        self.tool_tip = tk.Toplevel(self.widget)
        self.tool_tip.wm_overrideredirect(True)
        self.tool_tip.wm_geometry('+%d+%d' % (x, y))
        label = tk.Label(self.tool_tip, text=self.tip, borderwidth=1, relief='solid')
        label.pack(ipadx=5)
        
    def __close(self, event=None):
        """
        The method to hide a tooltip.

        Parameters
        ----------
        event : Event, optional
            The event indicating a leave. The default is None.

        Returns
        -------
        None.

        """
        if self.tool_tip:
            self.tool_tip.destroy()