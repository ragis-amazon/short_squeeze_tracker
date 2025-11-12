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
import re
from dotenv import load_dotenv

class FinvizScraper:
    def __init__(self):
        load_dotenv()
        self.username = os.getenv("FINVIZ_USERNAME")
        self.password = os.getenv("FINVIZ_PASSWORD")
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
            # chrome_options.add_argument("--headless=new")  # Disable headless for debugging
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--disable-popup-blocking")
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            
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
            
            # Set page load timeout
            self.driver.set_page_load_timeout(30)
            
        except Exception as e:
            error_msg = f"Failed to initialize Chrome WebDriver: {str(e)}\n"
            error_msg += "Please make sure Chrome is installed on your system.\n"
            error_msg += "You can download Chrome from: https://www.google.com/chrome/"
            raise Exception(error_msg)
        
    def close_all_ads(self, max_attempts=10):
        """Try to close all visible ads/popups on the page."""
        close_selectors = [
            (By.CLASS_NAME, "modal_close"),
            (By.CLASS_NAME, "close"),
            (By.XPATH, "//div[contains(@class, 'modal')]//span[text()='×']"),
            (By.XPATH, "//div[contains(@class, 'modal')]//button[text()='Close']"),
            (By.XPATH, "//span[text()='×']"),
            (By.XPATH, "//button[text()='Close']"),
            (By.XPATH, "//div[contains(@id, 'ad_') or contains(@class, 'ad_')]//span[text()='×']"),
            (By.XPATH, "//div[contains(@id, 'ad_') or contains(@class, 'ad_')]//button[text()='Close']"),
            (By.XPATH, "//iframe[contains(@id, 'ad') or contains(@name, 'ad') or contains(@src, 'ad')]")
        ]
        for attempt in range(max_attempts):
            ad_closed = False
            for selector_type, selector_value in close_selectors:
                try:
                    close_btns = self.driver.find_elements(selector_type, selector_value)
                    for btn in close_btns:
                        if btn.is_displayed() and btn.is_enabled():
                            print(f"Attempt {attempt+1}: Closing ad/modal with selector: {selector_value}")
                            btn.click()
                            time.sleep(2)
                            ad_closed = True
                except Exception:
                    continue
            # Take a screenshot after each attempt
            self.driver.save_screenshot(f"finviz_debug_ads_attempt_{attempt+1}.png")
            print(f"Saved screenshot as finviz_debug_ads_attempt_{attempt+1}.png")
            if not ad_closed:
                break
            time.sleep(2)

    def is_valid_ticker(self, ticker):
        """Return True if ticker looks like a valid stock symbol."""
        return bool(re.match(r'^[A-Z0-9.-]{1,10}$', ticker))

    def login(self):
        self.driver.get("https://finviz.com/login.ashx")
        time.sleep(2)
        self.driver.find_element(By.NAME, "email").send_keys(self.username)
        self.driver.find_element(By.NAME, "password").send_keys(self.password)
        self.driver.find_element(By.XPATH, "//input[@type='submit']").click()
        time.sleep(3)
        print("Logged in to Finviz")

    def get_top_shorted_stocks(self, num_stocks=20):
        """Get top most shorted stocks from Finviz (fetches visible rows, paginates if needed)"""
        self.login()
        try:
            self.driver.get("https://finviz.com/screener.ashx?v=152&o=-shortinterestshare")
            time.sleep(10)  # Increased wait time for page load
            print(f"Current URL: {self.driver.current_url}")

            # Close all ads/popups
            self.close_all_ads(max_attempts=10)

            # Find all tables, look for the one with the correct header
            tables = self.driver.find_elements(By.TAG_NAME, "table")
            target_table = None
            header_row = None
            header_map = {}
            for table in tables:
                header_candidates = table.find_elements(By.TAG_NAME, "tr")
                for row in header_candidates:
                    headers = [th.text.strip() for th in row.find_elements(By.TAG_NAME, "td") + row.find_elements(By.TAG_NAME, "th")]
                    lower_headers = [h.lower() for h in headers]
                    if 'ticker' in lower_headers and 'company' in lower_headers and 'short float' in lower_headers:
                        target_table = table
                        header_row = row
                        header_map = {h.lower(): i for i, h in enumerate(headers)}
                        break
                if target_table:
                    break
            if not target_table or not header_row or not header_map:
                print("Could not find the stock table or header!")
                self.driver.save_screenshot("finviz_debug.png")
                print("Saved screenshot as finviz_debug.png")
                print("Page source preview:", self.driver.page_source[:2000])
                return []

            # Scroll header into view
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", header_row)
            time.sleep(2)
            self.driver.save_screenshot("finviz_debug.png")
            print("Scrolled to header and saved screenshot as finviz_debug.png")

            # Define which fields to extract and their header names
            field_map = {
                'ticker': 'ticker',
                'company': 'company',
                'sector': 'sector',
                'industry': 'industry',
                'country': 'country',
                'market_cap': 'market cap.',
                'pe': 'p/e',
                'short_float': 'short float',
                'short_ratio': 'short ratio',  # Days to cover
                'short_interest': 'short interest',
                'volume': 'volume',
                'price': 'price',
                'change': 'change'
            }

            stocks = []
            page = 1
            while len(stocks) < num_stocks:
                rows = target_table.find_elements(By.TAG_NAME, "tr")[1:]  # skip header
                print(f"Page {page}: Found {len(rows)} stock rows")
                for row in rows:
                    cols = row.find_elements(By.TAG_NAME, "td")
                    if len(cols) < len(header_map):
                        continue
                    ticker = cols[header_map.get(field_map['ticker'], -1)].text.strip()
                    if not self.is_valid_ticker(ticker):
                        continue
                    stock = {}
                    for key, header in field_map.items():
                        idx = header_map.get(header.lower(), -1)
                        stock[key] = cols[idx].text.strip() if idx != -1 else ''
                    stocks.append(stock)
                    if len(stocks) >= num_stocks:
                        break
                if len(stocks) >= num_stocks:
                    break
                # Try to click next page if available
                try:
                    next_btn = self.driver.find_element(By.XPATH, "//a[contains(text(),'next') or contains(text(),'Next')]")
                    if next_btn.is_enabled():
                        print("Clicking next page...")
                        next_btn.click()
                        time.sleep(3)
                        page += 1
                    else:
                        print("Next button not enabled, stopping.")
                        break
                except Exception as e:
                    print(f"No next button found or error clicking next: {str(e)}")
                    break
            print(f"Successfully processed {len(stocks)} stocks")
            return stocks[:num_stocks]
        except Exception as e:
            print(f"Error getting top shorted stocks: {str(e)}")
            self.driver.save_screenshot("finviz_debug.png")
            print("Saved screenshot as finviz_debug.png")
            print("Page source preview:", self.driver.page_source[:2000])
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