# Amazon Bestsellers Scraper

A robust Python script for scraping Amazon's bestsellers pages. This tool retrieves comprehensive product details including names, prices, ratings, and review counts from Amazon's bestseller categories. Perfect for data analysis, market research, or tracking popular products.

## Features

* **Comprehensive Data Collection**

  * Supports Amazon.ae, Amazon.eg, Amazon.sa, and Amazon.com domains
  * Scrapes Amazon.eg and Amazon.sa product details in Arabic
  * Extracts comprehensive product information, including product name, category, price, rating, and more
  * Covers over 10 different categories
  * Up to 60 top products per category
  * Automatic scraping of all available bestseller categories

* **Robust Scraping Capabilities**
  * User-agent rotation to prevent blocking
  * Proxy support with automatic rotation
  * Configurable request delays
  * Built-in rate limiting and error handling
  * Progress bar for tracking scraping status

* **Flexible Output**
  * CSV file export with customizable naming
  * Detailed logging of the scraping process
  * Organized data structure for easy analysis

## Prerequisites

* Python 3.x
* Required packages (with versions):
  * beautifulsoup4 (4.11.1)
  * requests (2.32.3)
  * pandas (2.2.3)
  * tqdm (4.64.1)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/amazon-bestsellers-scraper.git
cd amazon-bestsellers-scraper
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

Run the scraper with default settings:
```bash
python amazon_scraper.py
```

### Advanced Usage

The script supports several command-line arguments for customization:

```bash
python amazon_scraper.py [--amazon_url URL] [--output FILENAME] [--min_sleep SECONDS] [--max_sleep SECONDS]
```

#### Command-line Arguments

* `--amazon_url`: Amazon domain to scrape (default: https://www.amazon.com)
* `--output`: Custom output CSV filename (default: amazon_bestsellers_YYYY-MM-DD.csv)
* `--min_sleep`: Minimum delay between requests in seconds (default: 4)
* `--max_sleep`: Maximum delay between requests in seconds (default: 10)

#### Examples

Scrape Amazon UK with custom output file:
```bash
python amazon_scraper.py --amazon_url https://www.amazon.co.uk --output uk_bestsellers.csv
```

Adjust request delays:
```bash
python amazon_scraper.py --min_sleep 5 --max_sleep 12
```

## Output Format

The script generates a CSV file with the following columns:

* `id`: Product identifier
* `category`: Bestseller category name
* `item`: Product name/title
* `price`: Product price
* `rating`: Product rating (out of 5 stars)
* `reviews`: Number of reviews
* `url`: Product page URL

Example output:
```csv
id,category,item,price,rating,reviews,url
B08N5KWB9H,Electronics,"Echo Dot (4th Gen)","$49.99","4.7 out of 5 stars","123,456",https://www.amazon.com/...
```

## Sample Data

Sample scraped data files are available in the `data` folder of this repository. You can examine these files to understand the data structure and format:

* `data/amazon_bestsellers_2024-11-04_arabic.csv` - Sample data from Arabic Amazon store
* Additional sample files with different dates showing historical bestseller data

These sample files can help you understand the output format and plan your data analysis.

## Troubleshooting

1. **Rate Limiting**
   * The script includes built-in delays between requests
   * Adjust `--min_sleep` and `--max_sleep` if you encounter blocking
   * Use different proxy settings if needed

2. **Connection Errors**
   * The script automatically retries failed requests
   * Check your internet connection
   * Verify proxy settings if using custom proxies

3. **Missing Data**
   * Some fields might show "Not Found" if the page structure changes
   * Check if the Amazon page structure has been updated

## Disclaimer

This script is for educational and personal use only. Web scraping may violate Amazon's terms of service. Use responsibly and check Amazon's policies before extensive use. The developers are not responsible for any misuse or terms of service violations.
