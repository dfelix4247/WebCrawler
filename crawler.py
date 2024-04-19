# needed arrow directions, which is why bs4/request used w/ pandas (hacky solution)
# best practice would be just pandas
# used gpt4 to frame solution
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os 

url = 'https://www.drayage.com/'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
table_rows = soup.find_all('tr')
column_data = []
start_row = 2
start_scraping = False

# iterate over each row, starting from the third row
for row in table_rows[start_row:]:
    row_data = [cell.text.strip() for cell in row.find_all('td')]

    img = row.find('img', src='https://www.loadmatch.com/images/arrow_black_horz.gif')

    if img and len(row_data) >= 3:  # make sure 'Arrow' column exists 
        row_data[2] = 'Right'
    elif len(row_data) >= 3:
        row_data[2] = 'Left'

    if len(row_data) == 14:
        start_scraping = True

    elif len(row_data) < 14 and start_scraping:
        break

    if row_data and start_scraping:
        column_data.append(row_data)

column_names = ['Terminal Name', 'Terminal', 'Arrow', 'Zip Code', 'State', 'City', 'FSC', 'FSC %', 
                'FSC Total', 'Notes', 'One-Way Miles', 'Per Mile (fuel incl)', 'Date','Blank']

df = pd.DataFrame(column_data, columns=column_names)

# cleaning
df['City'] = df['City'].str.removesuffix(' ()')
df['Per Mile (fuel incl)'] = df['Per Mile (fuel incl)'].str.removeprefix('$').astype(float)
df['FSC %'] = df['FSC %'].str.removesuffix('%').astype(float) / 100
df['One-Way Miles'] = df['One-Way Miles'].str.extract('^(.+) miles').astype(float)
df['FSC Total'] = df['FSC Total'].str.replace(r'\s+', '', regex=True)
df['FSC Total'] = df['FSC Total'].str.removeprefix('=$').astype(float)
df["Date"] = pd.to_datetime(df["Date"])
df = df.drop('Blank', axis = 1)

# load old data
os.chdir('/Users/')
prev_df = pd.read_csv('data.csv')

# update to new sheet
updated_df = pd.concat([df, prev_df]).drop_duplicates()

updated_df.to_csv('data.csv', index=False)
