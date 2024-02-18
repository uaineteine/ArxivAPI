print("[print_status] importing libraries")
from bs4 import BeautifulSoup
import requests
import re

def scrape_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Scrape information from div with class 'container container-md'
    container = soup.find('div', {'class': 'container container-md'})

    # Find the current status section and extract the status message
    current_status_section = container.find('section', {'id': 'current-status'})
    status_message = current_status_section.find('h2').text

    # Use regex to find the status message
    match = re.search(r'All systems are go', status_message)

    if match:
        print("[print_status] Main Status: All systems are go")
    else:
        print("[print_status] Main Status: Not found")

    # Find every child from ul with class 'list-components' 
    # that is an li tag with class 'list-component has-nested-components'
    list_items = soup.find('ul', {'class': 'list-components'}).find_all('li', {'class': 'list-component has-nested-components'})
    
    for item in list_items:
        print(item)

# Call the function with your URL
scrape_info('https://status.arxiv.org/')
