import os
import sys
from src.main import StockShortsTracker
import tkinter as tk
import argparse
from src.main import StockTrackerApp

def main():
    parser = argparse.ArgumentParser(description='Stock Shorts Tracker')
    parser.add_argument('--update-only', action='store_true',
                      help='Run only the data update without GUI')
    args = parser.parse_args()

    if args.update_only:
        app = StockTrackerApp()
        app.update_data()
    else:
        app = StockTrackerApp()
        app.run()

if __name__ == "__main__":
    main() 