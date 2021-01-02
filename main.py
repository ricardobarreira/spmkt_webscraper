import db_connection
from scraper import get_html, scrape_info


db_session = db_connection.create_session()

grocery_stores = ['rewe', 'kaufland']

for store in grocery_stores:
    # Get information needed to scrape store's website
    headers = db_connection.get_headers(db_session, store)
    urls = db_connection.get_urls(db_session, store)
    html_elements = db_connection.get_store_html_elements(db_session, store)

    offers_list = []
    for url in urls:
        # Get HTML data from the webpage
        source = get_html(url, headers)
        # Parse the HTML data into a HTML Class from the requests_html module
        offers_list.extend(scrape_info(source, html_elements))
    db_connection.update_local_database(store, offers_list, db_session)
