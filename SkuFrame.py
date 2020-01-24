from tkinter import *
from tkinter import colorchooser

class SkuFrame(Frame):
    #COLOR PICKER
    def colorpick(self):
        colorval = colorchooser.askcolor(title="Pick a Color")
        self.color = colorval[1]                                          
        self.btn_color.config(bg=self.color)

    def undo(self):
        if(self.counter > 0):
            #the line below actually works
            self.master.master.master.master.master.canvas.delete(self.circles[self.counter-1])
            self.circles.pop(self.counter-1)
            self.drawings.pop(self.counter-1)
            self.counter -= 1
            self.cntr_label.config(text="Count:"+str(self.counter))

    def __init__(self, master, **opt):
        self.master = master
        Frame.__init__(self, master, opt)

        #default values for variables
        self.color = 'blue'
        self.circles = [] 
        self.counter = 0
        self.drawings = []
        self.sku = StringVar()
        self.image_path = ""

        self.sku_label = Label(self, text='SKU')
        self.sku_label.grid(row='0', column='0', padx=3, pady=3)

        self.entry = Entry(self, textvariable=self.sku)
        self.entry.grid(row='1', column='0', padx=3, pady=3)

        self.btn_color = Button(self, text="Color", command=self.colorpick, bg=self.color)
        self.btn_color.grid(row='1', column='1', padx=3, pady=3)

        self.btn_undo = Button(self, text="Undo", command=self.undo)
        self.btn_undo.grid(row='2', column='0', padx=3, pady=3)

        self.cntr_label = Label(self, text="Count:"+str(self.counter))
        self.cntr_label.grid(row='2', column='1', padx=3, pady=3)
    
    