import requests
from bs4 import BeautifulSoup

# URL of the webpage
url = "https://www.synonymer.se/sv-syn/kumulativ"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the specific div element with the class 'synonymer-li-underline'
    target_div = soup.find("div", class_="synonymer-li-underline")

    # Check if the div element was found
    if target_div:
        # Find all <a> elements within the div and extract their text
        synonyms = [a.text for a in target_div.find_all("a")]
        
        # Print the synonyms
        print("Synonyms:", synonyms)
    else:
        print("Target div not found on the page.")
else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)
