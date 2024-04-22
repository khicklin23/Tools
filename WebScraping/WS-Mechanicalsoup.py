import mechanicalsoup
import pandas as pd
import matplotlib.pyplot as plt

# Define the URL
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#S&P_500_component_stocks"

# Initialize MechanicalSoup Browser
browser = mechanicalsoup.Browser()

# Get HTML content
response = browser.get(url)

# Extracting data from the table
table = response.soup.find('table', {'class': 'wikitable sortable'})

data = []
rows = table.find_all('tr')
for row in rows[1:]:
    columns = row.find_all('td')
    columns = [column.text.strip() for column in columns]
    data.append(columns)

# Convert data to DataFrame
columns = ["Symbol", "Security", "GICS Sector", "GICS Sub-Industry", "Headquarters", "Date added", "CIK", "Founded"]
df = pd.DataFrame(data, columns=columns)

# Save data to CSV
df.to_csv('MechanicalSoupWebScraping.csv', index=False)

# Plotting
sector_counts = df['GICS Sector'].value_counts()
sorted_sector_counts = sector_counts.sort_values(ascending=False)
top_sectors = sorted_sector_counts.head(5)
total_companies = df.shape[0]
top_sector_percentages = (top_sectors / total_companies) * 100

plt.figure(figsize=(10, 6))
plt.pie(top_sector_percentages, labels=top_sector_percentages.index, autopct='%1.1f%%')
plt.axis('equal')
plt.title('Top 5 GICS Sectors in S&P 500 Companies')
plt.show()

print(df)
