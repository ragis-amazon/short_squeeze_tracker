import os
import sys
from src.main import StockShortsTracker
import tkinter as tk
import argparse

def main():
    parser = argparse.ArgumentParser(description='Stock Shorts Tracker')
    parser.add_argument('--update-only', action='store_true',
                      help='Run only the data update without GUI')
    args = parser.parse_args()

    if args.update_only:
        app = StockShortsTracker(tk.Tk())
        app.scan_now()
    else:
        root = tk.Tk()
        app = StockShortsTracker(root)
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        root.mainloop()

if __name__ == "__main__":
    main() 