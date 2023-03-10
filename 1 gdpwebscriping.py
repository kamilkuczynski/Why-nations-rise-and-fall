from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
import numpy as np

wikiurl = "https://en.wikipedia.org/wiki/List_of_countries_by_past_and_projected_GDP_(PPP)_per_capita"
response = requests.get(wikiurl)

soup = BeautifulSoup(response.text, 'html.parser')

tables = soup.find_all('table', {'class': 'wikitable'})


for i, table in enumerate(tables):
    df = pd.read_html(str(table), header=0)[0]
    df = df.rename(columns={df.columns[0]: "Country"})
    df = df.replace('—', np.nan)
    df[df.columns.difference(['Country'])] = df[df.columns.difference(['Country'])].apply(pd.to_numeric, errors='coerce')
    print(f"Table {i + 1} has {df.duplicated().sum()} duplicate rows")
    print(f"Table {i + 1} has {df.isnull().sum()} missing values")
    missing_values_by_country = df.isnull().sum(axis=1).groupby(df['Country']).sum()
    print(missing_values_by_country)
    df.to_csv(f'1.{i} gdp_per_capita_{i}.csv', index=True, quoting=csv.QUOTE_NONNUMERIC)
