
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
indiatable=soup.find_all('table',{'class':"wikitable"})


df=pd.read_html(str(indiatable))
#print(df)

# rename columns for ease


# convert list to dataframe
#for i in range()
df=pd.DataFrame(df[0])

df = df.rename(columns={"Country (or dependent territory)": "Country"})
print(df.head(50))

df.to_csv('gdp_per_capita.csv', index=True, mode='a', quoting=csv.QUOTE_NONNUMERIC)

'''
import csv
with open("gdp_per_capita.csv", "a") as csv_file:
    writer = csv.writer(csv_file)
    for row in df:
        cols = row.find_all('td') # in html a column is represented by the tag <td>
        language_name = cols[1].getText() # store the value in column 3 as color_name
        annual_average_salary = cols[3].getText() # store the value in column 4 as color_code
        ## now we will write data to the file
        writer.writerow([language_name, annual_average_salary])
'''
