from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime
import time
import os
import sys
import requests
import zipfile
import io
import platform

class FinvizScraper:
    def __init__(self):
        self.setup_driver()
        
    def download_chromedriver(self):
        """Download and setup ChromeDriver for Mac ARM64"""
        # Create directory for ChromeDriver if it doesn't exist
        driver_dir = os.path.expanduser("~/.chromedriver")
        os.makedirs(driver_dir, exist_ok=True)
        
        # ChromeDriver version for Mac ARM64 (matching Chrome version 137)
        version = "137.0.7151.70"
        url = f"https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/{version}/mac-arm64/chromedriver-mac-arm64.zip"
        
        # Download and extract ChromeDriver
        response = requests.get(url)
        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_file:
            zip_file.extractall(driver_dir)
        
        # Set permissions
        driver_path = os.path.join(driver_dir, "chromedriver-mac-arm64", "chromedriver")
        os.chmod(driver_path, 0o755)
        
        return driver_path
        
    def setup_driver(self):
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            
            # Try to find Chrome in common macOS locations
            chrome_paths = [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/Applications/Chrome.app/Contents/MacOS/Chrome"
            ]
            
            chrome_path = None
            for path in chrome_paths:
                if os.path.exists(path):
                    chrome_path = path
                    break
                    
            if chrome_path:
                chrome_options.binary_location = chrome_path
            
            # Download and setup ChromeDriver
            driver_path = self.download_chromedriver()
            
            # Create service with specific executable path
            service = Service(executable_path=driver_path)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
        except Exception as e:
            error_msg = f"Failed to initialize Chrome WebDriver: {str(e)}\n"
            error_msg += "Please make sure Chrome is installed on your system.\n"
            error_msg += "You can download Chrome from: https://www.google.com/chrome/"
            raise Exception(error_msg)
        
    def get_top_shorted_stocks(self):
        """Get top 20 most shorted stocks from Finviz"""
        try:
            self.driver.get("https://finviz.com/screener.ashx?v=152&o=-shortinterestshare")
            time.sleep(2)  # Wait for page to load
            
            # Wait for the table to be present
            table = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "table-light"))
            )
            
            # Get all rows except header
            rows = table.find_elements(By.TAG_NAME, "tr")[1:21]  # Get first 20 rows
            
            stocks = []
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                if len(cols) >= 2:
                    ticker = cols[1].text
                    company = cols[2].text
                    sector = cols[3].text
                    industry = cols[4].text
                    short_interest = cols[6].text
                    stocks.append({
                        'ticker': ticker,
                        'company': company,
                        'sector': sector,
                        'industry': industry,
                        'short_interest': short_interest
                    })
            
            return stocks
            
        except Exception as e:
            print(f"Error getting top shorted stocks: {str(e)}")
            return []
            
    def get_stock_details(self, ticker):
        """Get short percentage and days to cover for a specific stock"""
        try:
            self.driver.get(f"https://finviz.com/quote.ashx?t={ticker}")
            time.sleep(2)
            
            # Find the short float and days to cover in the snapshot table
            snapshot_table = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "snapshot-table2"))
            )
            
            short_float = None
            days_to_cover = None
            
            # Get all rows in the snapshot table
            rows = snapshot_table.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                cols = row.find_elements(By.TAG_NAME, "td")
                for i, col in enumerate(cols):
                    if col.text == "Short Float":
                        short_float = cols[i+1].text
                    elif col.text == "Days to Cover":
                        days_to_cover = cols[i+1].text
            
            return {
                'ticker': ticker,
                'short_float': short_float,
                'days_to_cover': days_to_cover,
                'date': datetime.now().strftime('%Y-%m-%d')
            }
            
        except Exception as e:
            print(f"Error getting details for {ticker}: {str(e)}")
            return None
            
    def save_to_csv(self, data, filename):
        """Save data to CSV file"""
        df = pd.DataFrame(data)
        if os.path.exists(filename):
            df.to_csv(filename, mode='a', header=False, index=False)
        else:
            df.to_csv(filename, index=False)
            
    def close(self):
        """Close the browser"""
        self.driver.quit() 