import requests 
from bs4 import BeautifulSoup as bs 
import pandas as pd 
import matplotlib.pyplot as plt

# get the html data from the url 
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#S&P_500_component_stocks"
response = requests.get(url)
html_content = response.content

# create a BeautifulSoup object for parsing 
soup = bs(html_content, 'html.parser')

# used to find the class of any tables; outputs is 'wikitable sortable' twice, representing both tables
# print('Classes of each table:')
# for table in soup.find_all('table'):
#     print(table.get('class'))

# finds the first table with the wikitable sortable class 
table = soup.find('table', {'class': 'wikitable sortable'})

# extract data from the table, skips header row 
data = [] 
rows = table.find_all('tr')
for row in rows[1:]: 
    columns = row.find_all('td')
    columns = [column.text.strip() for column in columns]
    data.append(columns)
    
# convert data to dataframe for plotting
columns = ["Symbol", "Security", "GICS Sector", "GICS Sub-Industry", "Headquarters", "Date added", "CIIK", "Founded"]
df = pd.DataFrame(data, columns=columns)

df.to_csv('BeautifulSoupWebScraping.csv', index=False)  


# plotting: 
# count the occurrences of each GICS Sector
sector_counts = df['GICS Sector'].value_counts()

# sort the sector counts in descending order
sorted_sector_counts = sector_counts.sort_values(ascending=False)

# get the top 5 GICS Sectors
top_sectors = sorted_sector_counts.head(5)

# calculate the total number of companies
total_companies = df.shape[0]

# calculate the percentage of each top sector
top_sector_percentages = (top_sectors / total_companies) * 100

# count the occurrences of each GICS Sector
sector_counts = df['GICS Sector'].value_counts()

# calculate the total number of companies
total_companies = df.shape[0]

# calculate the percentage of each GICS Sector
sector_percentages = (sector_counts / total_companies) * 100

# add the percentage as a new column to the dataframe
df['Percentage'] = df['GICS Sector'].map(sector_percentages)

# sort the dataframe by the 'Percentage' column in descending order
df = df.sort_values(by='Percentage', ascending=False)

top_sectors = df['GICS Sector'].value_counts().head(5)
top_sector_percentages = (top_sectors / df.shape[0]) * 100

# create a pie chart
plt.figure(figsize=(10, 6))
plt.pie(top_sector_percentages, labels=top_sector_percentages.index, autopct='%1.1f%%')
plt.axis('equal')  # Equal aspect ratio ensures the pie chart is drawn as a circle.
plt.title('Top 5 GICS Sectors in S&P 500 Companies')
plt.show()
df 