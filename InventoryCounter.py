#try this

import cv2
import SkuFrame
import ScrollableFrame
from tkinter import *
from tkinter import filedialog
from PIL import Image
from PIL import ImageTk
from PIL import ImageDraw

class MainWindow(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        self.master = master
        #CANVAS
        self.c_width = master.winfo_screenwidth()-270
        self.c_height = master.winfo_screenheight()*11/12
        self.canvas = Canvas(self, width = self.c_width, height = self.c_height, bg = 'pink')
        self.canvas.grid(row='1', columnspan='4')
        
        #IMAGE BUTTON
        btn_openimg = Button(self, text="Open Image", command=self.open_image)
        btn_openimg.grid(row='0', column='0')

        #SAVE BUTTON
        btn_save = Button(self, text="Save Image", command=self.save)
        btn_save.grid(row='0', column='1')
        
        self.set_up_sku()


    def set_up_sku(self):

         #SKU FRAME
        self.right_frame = Frame(self)
        self.right_frame.grid(row='1', column='5') 
        self.sku_list = []
        self.items_frame = ScrollableFrame.ScrollableFrame(self.right_frame)
        self.items_frame.canvas.config(width = self.master.winfo_screenwidth()*1/8, height= self.master.winfo_screenheight()*11/12)
        self.items_frame.pack(fill="both")

        #ADD NEW SKU BUTTON
        self.btn_add_frame = Button(self.items_frame.scrollable_frame, width = "20", text="+", command=self.add_sku)
        self.btn_add_frame.grid(row = '1000', column = '1', pady=3)

        #FIRST RADIO BUTTON FOR SKUS
        self.rb_var = IntVar()
        self.rb = Radiobutton(self.items_frame.scrollable_frame, text = len(self.sku_list) + 1, indicatoron=0, padx = 20, variable = self.rb_var, command = self.pick_sku, value = len(self.sku_list))
        self.rb.grid(row = len(self.sku_list), column = '0')

        #FIRST SKU FRAME ENTRY ON THE RIGHT
        first_sku = SkuFrame.SkuFrame(self.items_frame.scrollable_frame)
        first_sku.grid(row= len(self.sku_list) , column = '1')
        self.sku_list.append(first_sku)
        self.curr_sku = self.sku_list[0]

    def open_image(self):
        self.canvas.delete("all")
        path = filedialog.askopenfilename(title = "Select file")

        #start with cv2 to have proper landscape or portrait image
        self.image = cv2.imread(path)
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

        #change type to pillow image
        self.pil_image = Image.fromarray(self.image)

        #calculate image position
        self.img_width, self.img_height = self.pil_image.size
        self.img_width_scaled = (int)(self.img_width*self.c_height/self.img_height-20)
        self.img_height_scaled = (int)(self.c_height-20)
        self.w_offset = (self.c_width - self.img_width_scaled)/2
        self.h_offset = 10
        self.pil_image = self.pil_image.resize((self.img_width_scaled, self.img_height_scaled))

        #put image in
        self.image = ImageTk.PhotoImage(self.pil_image) 
        self.draw = ImageDraw.Draw(self.pil_image)
        self.canvas.create_image(self.c_width/2, self.c_height/2, image = self.image, anchor = CENTER)
        self.canvas.bind('<Button-1>', self.paint)

        self.set_up_sku()

    def save(self):
        filename = filedialog.asksaveasfilename(title = "Save file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))

        for i in range(len(self.sku_list)):
            for j in range(len(self.sku_list[i].drawings)):
                x = self.sku_list[i].drawings[j][0] 
                y = self.sku_list[i].drawings[j][1] 
                c = self.sku_list[i].drawings[j][2]
                self.draw.ellipse((x-5, y-5, x+5, y+5), fill=c)
        self.pil_image.save(filename)

    def add_sku(self):
        new_sku = SkuFrame.SkuFrame(self.items_frame.scrollable_frame)
        new_sku.grid(row= len(self.sku_list) , column = '1')
        rb = Radiobutton(self.items_frame.scrollable_frame, width = '0', text = len(self.sku_list) + 1, indicatoron=0, padx = 20, command = self.pick_sku, variable = self.rb_var, value = len(self.sku_list))
        rb.grid(row = len(self.sku_list), column = '0')
        self.sku_list.append(new_sku)

    def pick_sku(self):
        self.curr_sku = self.sku_list[self.rb_var.get()]
    
    def paint(self, event):
        x, y = (event.x), (event.y)
        c_circle = self.canvas.create_oval((x-5, y-5, x+5, y+5), fill=self.curr_sku.color)
        self.curr_sku.circles.insert(self.curr_sku.counter,c_circle)
        x1 = x - self.w_offset
        y1 = y - self.h_offset
        curr_color = self.curr_sku.color
        self.curr_sku.drawings.insert(self.curr_sku.counter, (x1, y1, curr_color)) 
        self.curr_sku.counter += 1
        self.curr_sku.cntr_label.config(text="Count:"+str(self.curr_sku.counter))

window = Tk()
window.state('zoomed')
frame = MainWindow(window)
frame.grid(row=0, column=0)
window.mainloop()