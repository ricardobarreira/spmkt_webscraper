import urllib.request
import urllib.error
import urllib.parse
from requests_html import HTML
import re


def get_html(url, headers):
    r = urllib.request.Request(url=url, method='GET', headers=headers)
    response = urllib.request.urlopen(r)
    print(f'{url} RESPONSE: {response.status}')
    return response.read()


def scrape_info(source, html_elements):
    """Returns a list of retrieved offers, with each element being a dict"""

    # Parse the HTML data into a HTML Class from the requests_html module
    data = [HTML(html=source)]

    # Divide html elements into two categories
    high_level_divs = [i for i in html_elements if i.h_level > 0]
    items_elements = [i for i in html_elements if i.h_level == 0]

    for div in high_level_divs:
        # Crawl into the HTML structure until reach items of interest level
        data = data[0].find(f'.{div.element_string}')

    # Initialize list that will hold dicts containing the offers
    offers_list = []
    for tag in data:
        temp_dict = {}

        for element in items_elements:
            try:
                text_data = tag.find(f'.{element.element_string}')[0].text

                # If the offer is from rewe, and the type is 'quantity', the retrieved text needs additional processing
                if element.store_id == 1 and element.type == 'quantity':
                    text_data = re.findall(r'je (.+)', text_data)[0]

                temp_dict[element.type] = text_data
            # Failure to retrieve any value from this tag
            # TODO specify exception
            except:
                temp_dict[element.type] = ""

        # Concatenates brand and title into titles for Kaufland offers
        if 'brand' in temp_dict.keys():
            temp_dict['title'] = f'{temp_dict["brand"]} {temp_dict["title"]}'.strip()
            del temp_dict["brand"]

        offers_list.append(temp_dict)

    return offers_list
