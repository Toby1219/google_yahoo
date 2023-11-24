import scrapy
from goog.items import GoogItem
import sqlite3


class GoogleSpider(scrapy.spiders.SitemapSpider):
    name = "google"
    allowed_domains = ["www.google.com"]
    sitemap_urls = ["https://www.google.com/finance/sitemap.xml"]
    sitemap_follow = ['/quote']
    sitemap_rules = [('/quote', 'parse')]

    custom_settings = {'FEEDS': {
        'stock_data/google.csv': {'format': 'csv'},
        'stock_data/google.json': {'format': 'json'}
    }}

    def parse(self, response):
        item = GoogItem()
        try:
            item['name'] = response.css('div.zzDege ::text').get(),
            item['stock_Value'] = response.css('div.fxKbKc ::text').get(),
            item['time'] = response.css('div.ygUjEc::text').get().replace('\u202f', ' ').strip(),
            item['previous_close'] = response.css('div.P6K39c ::text').get(),
            item['day_range'] = response.css('div.P6K39c ::text').getall()[1],
            item['volume'] = response.css('div.P6K39c ::text').getall()[2],
            item['market_segment'] = response.css('div.P6K39c ::text').getall()[4],
            item['info'] = response.css('div.bLLb2d::text').get().replace('\n', ' ').strip()

            yield item
            self.save_to_database(data=item)
        except:
            pass

    def save_to_database(self, data):
        connection = sqlite3.connect('stock_data/google.db')
        cursor = connection.cursor()
        try:
            # Create a table if it doesn't exist
            cursor.execute('''
                            CREATE TABLE IF NOT EXISTS scraped_data (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT,
                                stock_Value INT,
                                time TEXT,
                                previous_close TEXT,
                                day_range TEXT,
                                volume TEXT,
                                market_segment TEXT,
                                info TEXT
                            )
                        ''')

            # Insert data into the table
            cursor.execute('''
                            INSERT INTO scraped_data (
                                name, stock_Value, time, previous_close,
                                day_range, volume, market_segment, info
                            )
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        ''',
                           (str(data['name']), str(data['stock_Value']), str(data['time']), str(data['previous_close']),
                            str(data['day_range']), str(data['volume']), str(data['market_segment']),
                            str(data['info'])))

            # Commit the changes
            connection.commit()
            self.log(f"Data successfully inserted into scraped_data")

        except sqlite3.Error as e:
            self.log(f"Error inserting data into google.db: {e}")

        finally:
            cursor.close()
            connection.close()
