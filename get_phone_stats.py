from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from ozon_phone.spiders.phones_spider import PhonesSpiders
import os
import pandas as pd

DATA_FILE_NAME = 'phone_data.csv'

MAX_SMARTPHONE = 100

if __name__ == "__main__":
    settings = get_project_settings()
    SETTING = {
        **settings,
        'FEEDS': {
            DATA_FILE_NAME: {
                'format': 'csv',
            }
        },
        'LOG_LEVEL': 'ERROR',
    }

    # for ozon.by
    # PhonesSpiders.start_urls = ['https://ozon.by/category/smartfony-15502/?sorting=rating']
    # PhonesSpiders.allowed_domains = ['ozon.by']
    # PhonesSpiders.PRODUCT_URL = 'https://ozon.by'

    PhonesSpiders.custom_settings = {
        'LOG_LEVEL': 'ERROR',
    }

    PhonesSpiders.MAX_SMARTPHONE = MAX_SMARTPHONE

    # delete old datafile
    if os.path.exists(DATA_FILE_NAME):
        os.remove(DATA_FILE_NAME)

    # run scrapy's spider
    process = CrawlerProcess(settings=SETTING)
    process.crawl(PhonesSpiders)
    process.start()

    # count os version
    # there isn't os version for some phones. os version for this phones set as unknown
    try:
        phone_stats = pd.read_csv(DATA_FILE_NAME)
        stats_os_version = phone_stats['os_version'].value_counts()
        print('COUNT PHONES OS VERSION:')
        print('-'*10)
        for i in stats_os_version.index:
            print(f'{i} - {stats_os_version[i]}')
        print('-' * 10)
        print(f'Total: {sum(stats_os_version)}')
    except Exception as e:
        print(f'WARNING: {e}')
