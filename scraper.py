import urllib.request
import urllib.error
import urllib.parse
from requests_html import HTML
import re


def get_html(url, headers):
    """Fetch data from the URL passed and return the HTML code

    Keyword arguments:
        url(string): a valid URL
        headers(dict): strings for keys and values

    Returns:
        string:Full HTML code from webpage
    """

    r = urllib.request.Request(url=url, method='GET', headers=headers)    # Request object
    response = urllib.request.urlopen(r)    # Bytes object with the data retrieved
    print(f'{url} RESPONSE: {response.status}')
    return response.read()


def scrape_data(source, html_tag_obj_list):
    """Take in HTML source code, find tags with data of interest, and return it in a list

    Keyword arguments:
        source(string): HTML code
        html_tag_obj_list(list): List elements are objects from the Html class in tables_objects module

    Returns:
        list:Each element is a dict containing offer attributes and their values
    """

    html_obj = [HTML(html=source)]     # Parse the HTML string into a HTML object from the requests_html module

    high_lvl_html_divs = [i for i in html_tag_obj_list if i.h_level > 0]   # parent-tags for all product-tags
    product_lvl_html_divs = [i for i in html_tag_obj_list if i.h_level == 0]

    for div in high_lvl_html_divs:    # Crawl into the HTML structure until products lvl is reached
        try:
            html_obj = html_obj[0].find(f'.{div.class_attr}')

        except:     # TODO define which exception to catch
            print("Could not access high level divs")

    offers_list = []
    for tag in html_obj:    # Iterates over all individual product tags
        tmp_dict = {}

        for div in product_lvl_html_divs:
            try:
                text_data = tag.find(f'.{div.class_attr}')[0].text

                if div.store_id == 1 and div.type == 'quantity':
                    text_data = re.findall(r'je (.+)', text_data)[0]    # Clean quantity string for rewe offers

                tmp_dict[div.type] = text_data
            except:     # TODO specify exception
                tmp_dict[div.type] = ""

        # Concatenates brand and title into one string for Kaufland offers
        if 'brand' in tmp_dict.keys():
            tmp_dict['title'] = f'{tmp_dict["brand"]} {tmp_dict["title"]}'.strip()
            del tmp_dict["brand"]

        offers_list.append(tmp_dict)

    return offers_list
