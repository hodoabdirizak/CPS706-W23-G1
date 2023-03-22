import tkinter as tk
from Edges import Page1

class Page2(tk.Frame):  
    def __init__(self, parent, controller):  
        tk.Frame.__init__(self, parent)  
        label = tk.Label(self, text="Page Two!!!", font=('calibre 10 bold'))  
        label.pack(pady=10,padx=10)  
  
        b1 = tk.Button(self, text="Go Back", command=lambda: controller.show_frame(Page1))  
        b1.pack()  