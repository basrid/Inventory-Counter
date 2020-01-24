import tkinter as tk
from tkinter import ttk


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        self.master = container
        self.canvas = tk.Canvas(self)
        self.counter = 0
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.canvas.bind('<MouseWheel>', self.scroll)
        self.canvas.pack(side="left", fill="both")
        scrollbar.pack(side="right", fill="y", anchor="w")
    
    def scroll(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    