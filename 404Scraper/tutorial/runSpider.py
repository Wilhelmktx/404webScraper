import argparse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from tutorial.spiders.quotes_spider import QuotesSpider

def main():
    parser = argparse.ArgumentParser(description='Run the spider.')
    # parser.add_argument('--page', type=int, default=1, help='Page number to scrape.')
    # parser.add_argument('--number', type=int, default=10, help='Number of links to scrape.')
    # args = parser.parse_args()

    process = CrawlerProcess(get_project_settings())
    process.crawl(QuotesSpider)
    process.start()

if __name__ == '__main__':
    main()