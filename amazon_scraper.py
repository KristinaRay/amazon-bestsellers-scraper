import argparse
import random
import requests
import time
from typing import Dict, List, Tuple, Optional

from tqdm import tqdm
from bs4 import BeautifulSoup
import pandas as pd
import logging
from datetime import date

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Define the headers list for user-agent rotation
HEADERS_LIST = [
    {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36"
    },
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0"
    },
    {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36"
    },
    {
        "User-Agent": "Mozilla/6.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Ubuntu/11.10 Chromium/27.0.1453.93 Chrome/27.0.1453.93 Safari/537.36"
    },
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36"
    },
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0)"
    },
    {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"},
    {"User-Agent": "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)"},
    {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"},
    {
        "User-Agent": "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11"
    },
    {
        "User-Agent": "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11"
    },
    {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
    },
    {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)"},
    {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"},
    {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"},
    {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)"},
    {
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)"
    },
    {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)"},
    {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)"},
    {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)"},
]

# Define the list of proxies
CHINA_PROXIES_LIST = [
    {"http": "http://123.56.169.22:3128"},
    {"http": "http://121.196.226.246:84"},
    {"http": "http://122.49.35.168:33128"},
    {"http": "http://124.238.235.135:81"},
    {"http": "http://121.40.199.105:80"},
    {"http": "http://202.99.99.123:80"},
    {"http": "http://61.153.67.110:9999"},
    {"http": "http://121.40.213.161:80"},
    {"http": "http://121.42.163.161:80"},
    {"http": "http://111.13.7.42:81"},
    {"http": "http://114.215.103.121:8081"},
    {"http": "http://175.11.157.195:80"},
]
USA_PROXIES_LIST = [
    {"http": "http://40.140.245.109:8080"},
    {"http": "http://50.116.12.78:8118"},
    {"http": "http://69.85.70.37:53281"},
    {"http": "http://35.195.160.37:1244"},
    {"http": "http://104.131.122.164:8118"},
    {"http": "http://32.115.161.78:53281"},
    {"http": "http://165.227.7.51:80"},
    {"http": "http://72.169.78.49:87"},
    {"http": "http://52.24.67.217:80"},
    {"http": "http://209.159.156.199:80"},
    {"http": "http://198.35.55.147:443"},
    {"http": "http://97.72.129.36:87"},
    {"http": "http://152.160.35.171:80"},
    {"http": "http://191.96.51.224:8080"},
    {"http": "http://45.55.157.204:80"},
]

ALL_PROXIES = CHINA_PROXIES_LIST + USA_PROXIES_LIST


def get_random_headers() -> Dict[str, str]:
    """Return a random user-agent header."""
    return random.choice(HEADERS_LIST)


def get_random_proxy() -> Dict[str, str]:
    """Return a random proxy from the combined proxy list."""
    return random.choice(ALL_PROXIES)


def get_links(amazon_url: str = "https://www.amazon.com") -> Tuple[List[str], List[str]]:
    """
    Fetches best seller category links from the Amazon Best Sellers page.

    Args:
        amazon_url (str): Base URL of Amazon's website. Defaults to "https://www.amazon.com".

    Returns:
        Tuple[List[str], List[str]]:
            A tuple containing:
            - List of URLs for each best seller category.
            - List of category names corresponding to those URLs.
    """
    logger.info(f"Fetching best seller categories from {amazon_url}")
    url = f"{amazon_url}/gp/bestsellers?ref_=nav_cs_bestsellers"
    try:
        response = requests.get(
            url, headers=get_random_headers(), proxies=get_random_proxy(), timeout=10
        )
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Failed to fetch best sellers page: {e}")
        return [], []

    content = BeautifulSoup(response.content, "html.parser")

    links_to_parse = []
    categories = []

    try:
        all_category_bestsellers = content.find_all(
            "div", {"data-card-metrics-id": "p13n-zg-nav-tree-all_zeitgeist-lists_1"}
        )[0].find_all("a")
    except (IndexError, AttributeError) as e:
        logger.error(f"Failed to parse best seller categories: {e}")
        return [], []

    for item in all_category_bestsellers:
        href = item.get("href")
        if href:
            links_to_parse.append(amazon_url + href)
            categories.append(item.get_text(strip=True))
    return links_to_parse, categories


def scrape_next_page(content: BeautifulSoup, amazon_url: str) -> Optional[str]:
    """
    Extracts the URL of the next page from the provided Amazon search results page content.

    Args:
        content (BeautifulSoup): The parsed HTML content of the Amazon search results page.
        amazon_url (str): Base URL of Amazon's website.

    Returns:
        Optional[str]: The URL of the next page if available, or None if there is no next page.
    """
    try:
        next_page_href = content.ul.find_all("a")[1]["href"]
        return amazon_url + next_page_href
    except (AttributeError, IndexError, TypeError):
        return None


def scrape_product_details(
    url: str,
    links_to_parse: List[str],
    categories: List[str],
    amazon_url: str = "https://www.amazon.com",
    max_retries: int = 3,
    sleep_range: Tuple[int, int] = (2, 10),
) -> List[Dict[str, str]]:
    """
    Scrapes product details from an Amazon Best Sellers page.

    Args:
        url (str): The URL of the Amazon category page to scrape.
        links_to_parse (List[str]): List of all category URLs to match the current category.
        categories (List[str]): List of category names corresponding to the URLs.
        amazon_url (str): Base URL of Amazon's website.
        max_retries (int): Number of retries for failed requests.
        sleep_range (Tuple[int, int]): Range of seconds to sleep between retries.

    Returns:
        List[Dict[str, str]]: List of product details dictionaries.
    """
    headers = get_random_headers()
    proxies = get_random_proxy()

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, proxies=proxies, timeout=10)
            response.raise_for_status()
            break
        except requests.RequestException as e:
            logger.warning(
                f"Request failed for {url} (attempt {attempt + 1}/{max_retries}): {e}"
            )
            time.sleep(random.uniform(*sleep_range))
    else:
        logger.error(f"Failed to retrieve {url} after {max_retries} attempts.")
        return []

    content = BeautifulSoup(response.content, "html.parser")

    try:
        index = links_to_parse.index(url)
        category = categories[index]
    except ValueError:
        category = "Unknown"

    item_details = []

    for item in content.select(".zg-grid-general-faceout"):
        data = {}
        try:
            data["id"] = item.select("div")[0].get("id", "Not Found")
        except (IndexError, AttributeError):
            data["id"] = "Not Found"

        data["category"] = category

        try:
            data["item"] = item.find("span").find("div").get_text(strip=True)
        except AttributeError:
            data["item"] = "Not Found"

        try:
            data["price"] = item.select("._cDEzb_p13n-sc-price_3mJ9Z")[0].get_text(strip=True)
        except (IndexError, AttributeError):
            data["price"] = "Not Found"

        try:
            data["rating"] = item.select(".a-icon-row i")[0].get_text(strip=True)
        except (IndexError, AttributeError):
            data["rating"] = "Not Found"

        try:
            data["reviews"] = item.select(".a-icon-row a")[0].select(".a-size-small")[0].get_text(strip=True)
        except (IndexError, AttributeError):
            data["reviews"] = "Not Found"

        try:
            href = item.select(".a-icon-row a")[0]["href"]
            data["url"] = amazon_url + href
        except (IndexError, KeyError, TypeError):
            data["url"] = "Not Found"

        item_details.append(data)

    return item_details


def main():
    parser = argparse.ArgumentParser(description="Scrape Amazon Best Sellers data")
    parser.add_argument(
        "--amazon_url",
        type=str,
        help="Amazon domain (default: https://www.amazon.com)",
        default="https://www.amazon.com",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output CSV file path (default: amazon_bestsellers_<date>.csv)",
        default=None,
    )
    parser.add_argument(
        "--min_sleep",
        type=int,
        help="Minimum sleep time between requests in seconds (default: 2)",
        default=4,
    )
    parser.add_argument(
        "--max_sleep",
        type=int,
        help="Maximum sleep time between requests in seconds (default: 10)",
        default=10,
    )
    args = parser.parse_args()

    amazon_url = args.amazon_url
    min_sleep = args.min_sleep
    max_sleep = args.max_sleep
    output_file = args.output

    logger.info("Scraping starts...")
    links_to_parse, categories = get_links(amazon_url)
    if not links_to_parse:
        logger.error("No categories found to scrape. Exiting.")
        return

    data = pd.DataFrame()
    today = date.today()

    for link in tqdm(links_to_parse, desc="Scraping categories"):
        scraped_data = scrape_product_details(
            link, links_to_parse, categories, amazon_url, sleep_range=(min_sleep, max_sleep)
        )
        if scraped_data:
            scraped_df = pd.DataFrame(scraped_data)
            data = pd.concat([data, scraped_df], ignore_index=True)
        time.sleep(random.uniform(min_sleep, max_sleep))

    if data.empty:
        logger.warning("No data scraped. CSV file will not be saved.")
    else:
        if not output_file:
            output_file = f"amazon_bestsellers_{today}.csv"
        data.to_csv(output_file, index=False)
        logger.info(f"Saved the results to CSV file: {output_file}")
        logger.info(f"Total products scraped: {len(data)}")


if __name__ == "__main__":
    main()
