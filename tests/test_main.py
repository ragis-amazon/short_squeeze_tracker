import pytest
from src.main import StockTrackerApp
import pandas as pd
import os

@pytest.fixture
def app():
    return StockTrackerApp()

def test_app_initialization(app):
    assert app is not None
    assert hasattr(app, 'scraper')
    assert hasattr(app, 'update_data')

def test_update_data(app):
    # Test data update
    app.update_data()
    
    # Verify files exist
    assert os.path.exists('data/top_shorted_stocks.csv')
    assert os.path.exists('data/stock_details.csv')
    
    # Verify data format
    stocks_df = pd.read_csv('data/top_shorted_stocks.csv')
    details_df = pd.read_csv('data/stock_details.csv')
    
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
    app.update_data()
    
    # Read both files
    stocks_df = pd.read_csv('data/top_shorted_stocks.csv')
    details_df = pd.read_csv('data/stock_details.csv')
    
    # Verify that all stocks in top_shorted_stocks.csv have corresponding entries in stock_details.csv
    stock_tickers = set(stocks_df['ticker'])
    detail_tickers = set(details_df['ticker'])
    
    assert stock_tickers.issubset(detail_tickers), "Some stocks are missing detailed information" 