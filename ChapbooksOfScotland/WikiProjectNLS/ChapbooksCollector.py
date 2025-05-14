import pickle
import re
from tqdm import tqdm

import requests
from bs4 import BeautifulSoup

from ChapbooksOfScotland.WikiProjectNLS.chapbook import Chapbook
from ChapbooksOfScotland.WikiProjectNLS.page import Page

wiki_project_url = "https://en.wikisource.org/wiki/Wikisource:WikiProject_NLS"

wikisource_base_url = "https://en.wikisource.org"

def fetch_chapbooks():
    # Fetch from the wiki project page
    response = requests.get(wiki_project_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # List of series elements
    series_elements = soup.find_all(id=re.compile("h-\w+-List_of_Works_Completed"))

    chapbooks = []
    for series_element in series_elements:
        series_name = series_element.next_element.text
        #print(series_name)
        # get top element wraps the series
        wrapper_element = series_element.parent.parent
        chapbooks_elements = wrapper_element.next_sibling.next_sibling.find_all("a")
        for chapbook_element in chapbooks_elements:
            #print(chapbooks_element)
            if "class" in chapbook_element and chapbook_element["class"] == "new":
                continue
            wikisource_url = wikisource_base_url + chapbook_element['href']
            title = chapbook_element['title']
            chapbook = Chapbook(wikisource_url=wikisource_url, series=series_name, title=title)
            chapbooks.append(chapbook)

    return chapbooks


def fetch_current_page_content(page_url):
    page_number = int(page_url.split("/")[-1])
    # Fetch from the wikisource page
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    categories_elements = soup.find(id="mw-normal-catlinks").find_all("li")
    categories = []
    for category_element in categories_elements:
        categories.append(category_element.text)
    paragraphs_elements = soup.find(id="mw-content-text").find_all("p")
    paragraphs = []
    for paragraph_element in paragraphs_elements:
        if paragraph_element.next_element.name is None:
            paragraph = paragraph_element.text
        else:
            paragraph = paragraph_element.next_element.text
        paragraph = paragraph.strip()
        paragraph = paragraph.replace("\n", " ")
        if paragraph != "":
            paragraphs.append(paragraph)
    page = Page(paragraphs=paragraphs, page_number=page_number, categories=categories)
    return page

def get_pages_for_chapbook(chapbook_title):
    page_number = 1
    page_base_url = wikisource_base_url + "/wiki/Page:" + chapbook_title.replace(" ", "_") + ".pdf/"
    page_url = page_base_url + str(page_number)
    pages = []
    while True:
        try:
            page = fetch_current_page_content(page_url)
            pages.append(page)
            page_number += 1
            page_url = page_base_url + str(page_number)
        except:
            break
    return pages

if __name__ == "__main__":
    # fetch all chapbooks
    all_chapbooks = fetch_chapbooks()
    # fetch pages for each chapbook
    for chapbook in tqdm(all_chapbooks):
        chapbook_title = chapbook.title
        pages = get_pages_for_chapbook(chapbook_title)
        chapbook.set_pages(pages)
    print(len(all_chapbooks[0].pages))
    # save the chapbooks in pickle file
    with open("chapbooks.pkl", "wb") as f:
        pickle.dump(all_chapbooks, f)
    # page_url = wikisource_base_url + "/wiki/Page:Accidents_and_disasters_on_land.pdf/2"
    # page = fetch_current_page_content(page_url)
    #
    # print(page.paragraphs)