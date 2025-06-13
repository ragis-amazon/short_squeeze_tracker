# Stock Shorts Tracker

A Python-based application that tracks and analyzes heavily shorted stocks using data from Finviz. The application provides a GUI interface to monitor short interest, track stock movements, and analyze potential short squeeze opportunities.

## Features

- Real-time tracking of top shorted stocks
- Detailed stock information including:
  - Short interest percentage
  - Days to cover
  - Company information
  - Sector and industry data
- Automatic daily updates
- User-friendly GUI interface
- Data export to CSV format

## Prerequisites

- Python 3.10 or higher
- Google Chrome browser
- Internet connection

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ragis-amazon/short_squeeze_tracker.git
cd short_squeeze_tracker
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python run.py
```

2. The GUI will open with the following options:
   - View top shorted stocks
   - Get detailed stock information
   - Export data to CSV
   - Set up automatic daily updates

## Project Structure

```
stock_shorts_tracker/
├── src/
│   ├── main.py          # Main application logic
│   ├── scraper.py       # Web scraping functionality
│   └── gui.py           # GUI implementation
├── data/                # Directory for storing CSV files
├── requirements.txt     # Project dependencies
└── run.py              # Application entry point
```

## Dependencies

- selenium==4.15.2
- pandas==2.1.3
- webdriver-manager==4.0.1
- python-dotenv==1.0.0
- schedule==1.2.1

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Data source: [Finviz](https://finviz.com)
- Built with Python and Selenium 