from db_connection import create_session, get_headers, get_urls, get_store_html_elements, update_local_database
from scraper import get_html, scrape_info


db_session = create_session()

grocery_stores = ['rewe', 'kaufland']

for store in grocery_stores:
    # Get information needed to scrape store's offers
    headers = get_headers(db_session, store)
    urls = get_urls(db_session, store)
    html_elements = get_store_html_elements(db_session, store)

    offers_list = []
    for url in urls:
        # Get HTML data from the webpage
        source = get_html(url, headers)
        # Parse the HTML data into a HTML Class from the requests_html module
        offers_list.extend(scrape_info(source, html_elements))
    update_local_database(store, offers_list, db_session)
