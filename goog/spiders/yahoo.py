import scrapy
from goog.items import YahooItem
import sqlite3


class YahooSpider(scrapy.spiders.SitemapSpider):
    name = "yahoo"
    # allowed_domains = ["www.finance.yahoo.com"]
    sitemap_urls = ["https://finance.yahoo.com/sitemaps/quotes/quote-1.xml"]
    sitemap_follow = ['/profile']
    sitemap_rules = [('/profile', 'parse')]

    custom_settings = {'FEEDS': {
        'stock_data/yahoo.csv': {'format': 'csv'},
        'stock_data/yahoo.json': {'format': 'json'}
    }}

    def parse(self, response):
        try:
            item = YahooItem()
            item['name'] = response.xpath('//div[@class="D(ib) "]/h1/text()').get()
            item['market_price'] = response.xpath(
                '//*[@id="quote-header-info"]/div[3]/div[1]/div/fin-streamer[1]/text()').get()
            item['market_change'] = \
            response.xpath('//fin-streamer[@data-field="regularMarketChange"]/span/text()').getall()[6]
            item['market_change_percent'] = response.xpath('//fin-streamer[3]/span/text()').get()
            item['time'] = response.xpath('//div[@id="quote-market-notice"]/span/text()').get()
            item['sector'] = response.xpath('//div[@data-test="qsp-profile"]/div/p[2]/span[2]/text()').get()
            item['industry'] = response.xpath('//div[@data-test="qsp-profile"]/div/p[2]/span[4]/text()').get()
            yield item
            self.save_to_database(data=item)
        except IndexError:
            pass

    def save_to_database(self, data):
        connection = sqlite3.connect('stock_data/yahoo_stock.db')
        cursor = connection.cursor()
        try:
            # Create a table if it doesn't exist
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS scraped_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, market_price TEXT, market_change TEXT,
                    market_change_percent TEXT, time TEXT,
                    sector TEXT, industry TEXT)
            ''')
            # Insert data into the table
            cursor.execute('''
                INSERT INTO scraped_data (
                    name, market_price, market_change, market_change_percent, time,
                    sector, industry)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (data['name'], data['market_price'], data['market_change'],
                  data['market_change_percent'], data['time'], data['sector'],
                  data['industry']))
            # Commit the changes
            connection.commit()
            self.log(f"Data successfully inserted into scraped_data")

        except sqlite3.Error as e:
            self.log(f"Error inserting data into yahoo_stock.db: {e}")

        finally:
            cursor.close()
            connection.close()
