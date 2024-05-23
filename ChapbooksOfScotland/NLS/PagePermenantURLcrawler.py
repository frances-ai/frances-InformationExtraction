import json
import re

import requests
from bs4 import BeautifulSoup


def fetch_page_permanent_url(url):
    page_url_list = {}
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the select tag with id "page_url"
        select_tag = soup.find('select', {"id": "page_url"})

        # Check if the select tag was found
        if select_tag:
            # Find all option tags within the select tag
            options = select_tag.find_all('option')

            # Extract and print the text of each option
            for option in options:
                option_value = option.get('value')
                option_text = option.text.strip()

                # Extract the number inside the first parenthesis
                match = re.search(r'\((\d+)\)', option_text)
                if match:
                    number = match.group(1)
                    print("Value:", option_value)
                    print("Page number:", number)
                    print()  # Print an empty line for better readability
                    page_url_list[number] = "https://digital.nls.uk/" + option_value
                else:
                    print("No number inside the first parenthesis found for option:", option_text)
        else:
            print("Select tag with id 'page_url' not found on the page.")
    else:
        print("Failed to fetch the page. Status code:", response.status_code)

    return page_url_list


def get_volumes_id(volumes_path_file):
    try:
        f = open(volumes_path_file, 'r')
        volume_paths = f.readlines()
        volume_ids = [path[(path.rfind("/")+1):].strip() for path in volume_paths]
        return volume_ids
    except Exception as e:
        print(str(e))
        return []


if __name__ == "__main__":
    # Get the volume ids
    volumes_path_file = "chapbook.txt"
    volume_ids = get_volumes_id(volumes_path_file)
    #print(volume_ids)

    # get the front page large image urls for each volume
    base_url = "https://digital.nls.uk/chapbooks-printed-in-scotland/archive/"
    volume_urls = [base_url + volume_id + "?mode=fullsize" for volume_id in volume_ids]
    #print(volume_urls)

    volume_page_urls = {}
    for index in range(len(volume_ids)):
        volume_id = volume_ids[index]
        volume_url = volume_urls[index]
        print(f"Fetching page urls from volume {volume_id} using url {volume_url}")
        page_urls = fetch_page_permanent_url(volume_url)
        print(f"there are {len(page_urls)} pages founded!")
        volume_page_urls[volume_id] = page_urls

    result_filename = "volume_page_urls.json"
    print(f"Saving the result to file: {result_filename}")

    with open(result_filename, "w") as f:
        json.dump(volume_page_urls, f)

    print(f"File saved!")
