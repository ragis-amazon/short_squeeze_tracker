import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import schedule
import time
from datetime import datetime
import os
import sys

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.scraper import FinvizScraper

class StockShortsTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Shorts Tracker")
        self.root.geometry("800x600")
        
        self.scraper = None
        self.is_running = False
        self.scheduler_thread = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Control buttons
        self.start_button = ttk.Button(main_frame, text="Start Tracking", command=self.start_tracking)
        self.start_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.stop_button = ttk.Button(main_frame, text="Stop Tracking", command=self.stop_tracking, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=5, pady=5)
        
        self.scan_button = ttk.Button(main_frame, text="Scan Now", command=self.scan_now)
        self.scan_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Log area
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="5")
        log_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=20, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var)
        status_bar.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
    def log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        
    def scan_now(self):
        try:
            if self.scraper is None:
                self.scraper = FinvizScraper()
                
            self.log("Starting scan...")
            self.status_var.set("Scanning...")
            
            # Get top 20 shorted stocks
            stocks = self.scraper.get_top_shorted_stocks()
            self.log(f"Found {len(stocks)} shorted stocks")
            
            # Save to CSV
            if stocks:
                self.scraper.save_to_csv(stocks, "top_shorted_stocks.csv")
                self.log("Saved top shorted stocks to CSV")
            
            # Get detailed information for each stock
            details = []
            for stock in stocks:
                detail = self.scraper.get_stock_details(stock['ticker'])
                if detail:
                    details.append(detail)
                    self.log(f"Got details for {stock['ticker']}")
            
            # Save detailed information
            if details:
                self.scraper.save_to_csv(details, "stock_details.csv")
                self.log("Saved detailed stock information to CSV")
            
            self.status_var.set("Scan completed")
            
        except Exception as e:
            error_msg = str(e)
            self.log(f"Error during scan: {error_msg}")
            self.status_var.set("Error during scan")
            
            # If there was an error with Chrome, show a more user-friendly message
            if "Failed to initialize Chrome WebDriver" in error_msg:
                self.log("\nPlease make sure Chrome is installed on your system.")
                self.log("You can download Chrome from: https://www.google.com/chrome/")
            
    def start_tracking(self):
        if not self.is_running:
            self.is_running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            
            # Schedule daily scan at 4:00 PM
            schedule.every().day.at("16:00").do(self.scan_now)
            
            # Start scheduler in a separate thread
            self.scheduler_thread = threading.Thread(target=self.run_scheduler)
            self.scheduler_thread.daemon = True
            self.scheduler_thread.start()
            
            self.log("Started daily tracking")
            self.status_var.set("Tracking active")
            
    def stop_tracking(self):
        if self.is_running:
            self.is_running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            
            schedule.clear()
            
            if self.scraper:
                self.scraper.close()
                self.scraper = None
            
            self.log("Stopped daily tracking")
            self.status_var.set("Tracking stopped")
            
    def run_scheduler(self):
        while self.is_running:
            schedule.run_pending()
            time.sleep(60)
            
    def on_closing(self):
        self.stop_tracking()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = StockShortsTracker(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop() 