import requests
from bs4 import BeautifulSoup

url = "https://news.ycombinator.com/"

response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')

    for index, link in enumerate(links, start=1):
        href = link.get('href')
        if href and ( href.startswith("http://") or href.startswith("https://")):
            title = link.text.strip()
            if title:
                print(f"{index}. {title}: {href}")
            else:
                print(f"{index}. No title found: {href}")    
else:
    print("Failed to fetch url")