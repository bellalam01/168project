# Scrapping the list of progamming languages 
# Output: a list of programming langugaes hyperlinks 

# import required modules
from bs4 import BeautifulSoup
import requests

# get URL
page = requests.get("https://en.wikipedia.org/wiki/List_of_programming_languages")
 
# scrape webpage
soup = BeautifulSoup(page.text, 'html.parser')

allLinks = soup.find(id="bodyContent").find_all("a")

for link in allLinks: 
    if link.has_key('href'):
        if link['href'].find("/wiki/") != -1: 
            print(link)