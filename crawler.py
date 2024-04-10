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

column_names = ['Terminal Name', 'Terminal', 'Arrow', 'Zip Code', 'State', 'Province', 'Seven', 'Eight', 
                'Total', 'Notes', 'One-Way Miles', 'Per Mile (fuel incl)', 'Date','Blank']

df = pd.DataFrame(column_data, columns=column_names)

os.chdir('/Users/')

prev_df = pd.read_csv('data.csv')

# update any new data to sheet
updated_df = pd.concat([df, prev_df]).drop_duplicates()

updated_df.to_csv('data.csv', index=False)
