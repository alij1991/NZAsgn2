import tkinter as tk
from drawing import PaintApp

root = tk.Tk()
root.geometry("1024x720")
root.resizable(False, False)
paint_app = PaintApp(root)
root.mainloop()
