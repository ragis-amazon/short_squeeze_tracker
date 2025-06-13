import os
import sys
from src.main import StockShortsTracker
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = StockShortsTracker(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop() 