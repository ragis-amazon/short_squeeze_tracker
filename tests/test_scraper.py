import pytest
from src.scraper import FinvizScraper
import pandas as pd
import os

@pytest.fixture
def scraper():
    return FinvizScraper()

def test_scraper_initialization(scraper):
    assert scraper is not None
    assert scraper.driver is not None

def test_get_top_shorted_stocks(scraper):
    stocks = scraper.get_top_shorted_stocks()
    assert isinstance(stocks, list)
    assert len(stocks) > 0
    for stock in stocks:
        assert 'ticker' in stock
        assert 'short_interest' in stock
        assert 'company_name' in stock
        assert 'sector' in stock
        assert 'industry' in stock

def test_get_stock_details(scraper):
    # Test with a known stock
    details = scraper.get_stock_details('AAPL')
    assert isinstance(details, dict)
    assert 'short_float' in details
    assert 'days_to_cover' in details

def test_save_to_csv(scraper):
    # Test data
    test_data = [
        {'ticker': 'TEST1', 'short_interest': '10.5', 'company_name': 'Test Company 1', 'sector': 'Tech', 'industry': 'Software'},
        {'ticker': 'TEST2', 'short_interest': '15.2', 'company_name': 'Test Company 2', 'sector': 'Finance', 'industry': 'Banking'}
    ]
    
    # Save test data
    scraper.save_to_csv(test_data, 'test_stocks.csv')
    
    # Verify file exists
    assert os.path.exists('test_stocks.csv')
    
    # Read and verify data
    df = pd.read_csv('test_stocks.csv')
    assert len(df) == 2
    assert 'ticker' in df.columns
    assert 'short_interest' in df.columns
    
    # Cleanup
    os.remove('test_stocks.csv')

def test_cleanup(scraper):
    scraper.cleanup()
    assert scraper.driver is None 