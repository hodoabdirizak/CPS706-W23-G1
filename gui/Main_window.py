import tkinter as tk  
from tkinter import Canvas
import re
  
class Container(tk.Tk):  
    def __init__(self, *args, **kwargs):  
        tk.Tk.__init__(self, *args, **kwargs)  
        container = tk.Frame(self)  
        container.pack(side="top", fill="both", expand = True)  
        container.grid_rowconfigure(0, weight=1)  
        container.grid_columnconfigure(0, weight=1)  
  
        self.frames = {}  
  
        for F in (Main_window, Page1, Page2):  
            frame = F(container, self)
            self.frames[F] = frame  
            frame.grid(row=0, column=0, sticky="nsew")  
  
        self.show_frame(Main_window)  
  
    def show_frame(self, cont):  
        frame = self.frames[cont]  
        frame.tkraise()  
  
class Main_window(tk.Frame):  
    def __init__(self, parent, controller):  
        tk.Frame.__init__(self,parent)  
        label = tk.Label(self, text="Enter input", font=('calibre 12 bold'))  
        label.pack(pady=10,padx=10)  
        button = tk.Button(self, text="Submit", command=lambda: controller.show_frame(Page1))  
        button.pack()   
  
  
class Page1(tk.Frame):  
  
    def __init__(self, parent, controller):  
        tk.Frame.__init__(self, parent)  
        label = tk.Label(self, text="Edges", font=('calibre 12 bold'))  
        label.pack(pady=10,padx=10)  
        button1 = tk.Button(self, text="Go Back to Input", command=lambda: controller.show_frame(Main_window))  
        button1.pack()  
        button2 = tk.Button(self, text="Submit",  
                            command=lambda: controller.show_frame(Page2))  
        button2.pack()  
  
  
class Page2(tk.Frame):  
    def __init__(self, parent, controller):  
        tk.Frame.__init__(self, parent)  
        label = tk.Label(self, text="Graph animation", font=('calibre 12 bold'))  
        label.pack(pady=10,padx=10)  
        button2 = tk.Button(self, text="Go Back to Edges", command=lambda: controller.show_frame(Page1))  
        button2.pack()  
          

window = Container()  
window.title('Routing Algorithm Visualization Tool')
window.geometry('800x600')
window.mainloop()  