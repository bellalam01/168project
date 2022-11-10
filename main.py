#Code to scrape all links from the link.txt file
#Return all data to data.csv file in format [title, influenced_by, influencedß]
import requests
from bs4 import BeautifulSoup
import csv
import re

def scrapeWiki(url):
    response = requests.get(url=url,)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find(id = "firstHeading")
    table = soup.find('table', {'class': 'infobox vevent'})
    influenced_by = ""
    influenced = ""
    if table:
        table_body = table.tbody
        rows = table_body.findAll(lambda tag: tag.name=='tr')
        for row in rows:
            if row.find(string = "Influenced by"):
                influenced_by = row.find_next_siblings('tr')
            elif row.find(string = "Influenced"):
                influenced = row.find_next_siblings('tr')
    print("=============================================")
    print(title.text)
    print("Influenced By :" + str(influenced_by))
    print("Influenced :" + str(influenced))
    print("=============================================")
    with open ('data.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        writer.writerow([title.text, influenced_by, influenced])
        csvfile.close()


with open ('link.txt', 'r') as txtfile:
    reader = csv.reader(txtfile)
    for rows in reader:
        for row in rows:
            link = re.findall('"([^"]*)"', row)
            scrapeWiki("https://en.wikipedia.org" + link[0])

txtfile.close()

