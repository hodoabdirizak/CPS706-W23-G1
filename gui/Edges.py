import tkinter as tk
from Main_window import Main_window
from Animation import Page2

class Page1(tk.Frame):  
    def __init__(self, parent, controller):  
        tk.Frame.__init__(self, parent)  
        label = tk.Label(self, text="Page One!!!", font=('calibre 10 bold'))  
        label.pack(pady=10,padx=10)  
  
        b1 = tk.Button(self, text="Go Back", command=lambda: controller.show_frame(Main_window))  
        b1.pack()  
  
        b2 = tk.Button(self, text="Submit", command=lambda: controller.show_frame(Page2))  
        b2.pack()  