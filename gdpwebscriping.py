
# https://medium.com/analytics-vidhya/web-scraping-a-wikipedia-table-into-a-dataframe-c52617e1f451
from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv

wikiurl = "https://en.wikipedia.org/wiki/List_of_countries_by_past_and_projected_GDP_(PPP)_per_capita"
response = requests.get(wikiurl)
#print(response.status_code)


# parse data from the html into a beautifulsoup object
soup = BeautifulSoup(response.text, 'html.parser')

tables = soup.find_all('table', {'class': 'wikitable'})


for i, table in enumerate(tables):
    df = pd.read_html(str(table))[0]
    print(f"Table {i + 1} has {df.duplicated().sum()} duplicate rows")
        print(f"Table {i + 1} has {df.isnull().sum()} missing values")
    df.to_csv(f'gdp_per_capita_{i}.csv', index=True, quoting=csv.QUOTE_NONNUMERIC)
