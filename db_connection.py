import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, desc
from tables_objects import Store, Headers, Cookies, Urls, Html, Products, Offers


# Config setting
def create_session(remote=False):
    if remote:
        engine = create_engine(os.getenv("DATABASE_URL"))
    else:
        engine = create_engine(f'mysql+pymysql://{os.getenv("MYSQL_USER")}:{os.getenv("MYSQL_PW")}@localhost/SuperMarket_data')
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def get_headers(session, store_name):
    """return a dict with data from the Headers and Cookies tables, both filtered by the store name"""

    headers_dict = {}
    headers = session.query(Headers).join(Store).filter(Store.store_name == store_name)
    for i in headers:
        headers_dict[i.header_type] = i.header_string

    cookie = session.query(Cookies).join(Store).filter(Store.store_name == store_name).first()
    headers_dict['cookie'] = cookie.cookie_string

    return headers_dict


def get_urls(session, store_name):
    """Return a list with all the URLs of the passed store"""

    urls_list = session.query(Urls).join(Store).filter(Store.store_name == store_name)
    return [i.url_string for i in urls_list]


def get_store_html_elements(session, store_name):
    """Return a list of Html objects"""

    html_elements = session.query(Html).join(Store).filter(Store.store_name == store_name).order_by(
        desc(Html.h_level)).all()
    return html_elements


def get_registered_products(session):
    query = session.query(Products.product_name, Products.product_quantity).all()
    # print([(i.product_name, i.product_quantity) for i in query])
    return query


def update_products(session, offers_list):
    #TODO add flag to differentiate calls to update local and remote databases in order to prevent unnecessary processing
    new_products = 0
    registered_products = get_registered_products(session)
    for offer in offers_list:
        if offer['title'] == "":
            continue
        if ((offer['title'], offer['quantity']) not in registered_products):
            new_products+=1

            product = Products(
                product_name=offer['title'],
                product_quantity=offer['quantity']
            )
            session.add(product)

    session.commit()
    print(50*'--',f"\n{new_products} new product(s) successfully committed\n", 50*'--')


def update_offers(session, store_id, offers_list):

    new_offers = 0
    for offer in offers_list:
        if offer['price'] == "":
            continue
        # Get product_id from Products table to register Foreign Key
        product_id = session.query(Products.product_id).filter(Products.product_name == offer['title']).first()
        offer = Offers(
            offer_discount=offer['discount'],
            offer_price=offer['price'],
            product_id=product_id[0],
            store_id=store_id
        )
        session.add(offer)
        new_offers += 1

    session.commit()
    print(50*'--',f"\n{new_offers} new offers successfully committed\n", 50*'--')

def clear_tables(session):
    """
    Clear all data from the products and offers tables so that the info available for the webapp contains only
    current offers and their respective products
    """
    products = session.query(Products).all()
    offers = session.query(Offers).all()

    for product, offer in zip(products, offers):
        session.delete(product)
        session.delete(offer)

    session.commit()


def update_local_database(store, offers_list, session):

    update_products(session, offers_list)

    if store == 'rewe':
        store_id = 1
    else:
        store_id = 2
    update_offers(session, store_id, offers_list)


def update_remote_database(store, offers_list, session, iter_number):
    if iter_number == 0:
        clear_tables(session)

    update_products(session, offers_list)

    if store == 'rewe':
        store_id = 1
    else:
        store_id = 2
    update_offers(session, store_id, offers_list)


if __name__ == '__main__':
    print(os.getenv("DATABASE_URL"))