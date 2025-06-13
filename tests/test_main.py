import pytest
from src.main import StockShortsTracker
import pandas as pd
import os
import tkinter as tk

@pytest.fixture
def app():
    root = tk.Tk()
    app = StockShortsTracker(root)
    yield app
    root.destroy()

def test_app_initialization(app):
    assert app is not None
    assert hasattr(app, 'scraper')
    assert hasattr(app, 'scan_now')

def test_scan_now(app):
    # Test data update
    app.scan_now()
    
    # Verify files exist
    assert os.path.exists('top_shorted_stocks.csv')
    assert os.path.exists('stock_details.csv')
    
    # Verify data format
    stocks_df = pd.read_csv('top_shorted_stocks.csv')
    details_df = pd.read_csv('stock_details.csv')
    
    assert len(stocks_df) > 0
    assert len(details_df) > 0
    
    # Verify required columns
    required_columns = ['ticker', 'short_interest', 'company_name', 'sector', 'industry']
    for col in required_columns:
        assert col in stocks_df.columns
    
    required_details = ['ticker', 'short_float', 'days_to_cover']
    for col in required_details:
        assert col in details_df.columns

def test_data_consistency(app):
    # Update data
    app.scan_now()
    
    # Read both files
    stocks_df = pd.read_csv('top_shorted_stocks.csv')
    details_df = pd.read_csv('stock_details.csv')
    
    # Verify that all stocks in top_shorted_stocks.csv have corresponding entries in stock_details.csv
    stock_tickers = set(stocks_df['ticker'])
    detail_tickers = set(details_df['ticker'])
    
    assert stock_tickers.issubset(detail_tickers), "Some stocks are missing detailed information" 