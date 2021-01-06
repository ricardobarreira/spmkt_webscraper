import db_connection
from scraper import get_html, scrape_info
import schedule
import time
from datetime import datetime
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('main.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# stream_handler = logging.StreamHandler()
# stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
# logger.addHandler(stream_handler)


def scrape_and_update():
    local_db_session = db_connection.create_session()
    remote_db_session = db_connection.create_session(remote=True)

    grocery_stores = ['rewe', 'kaufland']

    for i in range(len(grocery_stores)):
        # Get information needed to scrape store's website
        headers = db_connection.get_headers(local_db_session, grocery_stores[i])
        urls = db_connection.get_urls(local_db_session, grocery_stores[i])
        html_elements = db_connection.get_store_html_elements(local_db_session, grocery_stores[i])

        offers_list = []
        for url in urls:
            # Get HTML data from the webpage
            source = get_html(url, headers)
            # Parse the HTML data into a HTML Class from the requests_html module
            offers_list.extend(scrape_info(source, html_elements))
        try:
            db_connection.update_local_database(grocery_stores[i], offers_list, local_db_session)
            logger.info(f'Successfully updated local database for store: {grocery_stores[i]}')
        except:
            logger.exception(f'Failed to update local database for the store: {grocery_stores[i]}')

        # Update Heroku's Postgres database
        try:
            db_connection.update_remote_database(grocery_stores[i], offers_list, remote_db_session, i)
            logger.info(f'Successfully updated remote database for store: {grocery_stores[i]}')
        except:
            logger.exception(f'Failed to update local database for the store: {grocery_stores[i]}')


    print(f"\n*****Last Update: {datetime.now()}*****\n")


if __name__ == '__main__':
    schedule.every().day.at('07:00').do(scrape_and_update)
    while (True):
        schedule.run_pending()
        time.sleep(1)
