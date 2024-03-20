import requests
from bs4 import BeautifulSoup
import pandas as pd
import os 

# base url - once you choose a specific location update this url
url = 'https://www.drayage.com/'
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

# find all table rows
table_rows = soup.find_all('tr')

# create a list to store column data
column_data = []

# determine the row to start from
start_row = 2

# flag to indicate when to start scraping
start_scraping = False

# iterate over each row, starting from the third row
for row in table_rows[start_row:]:
    # extract data from each cell in the row
    row_data = [cell.text.strip() for cell in row.find_all('td')]

    # find an img tag with the specific src attribute within the row
    img = row.find('img', src='https://www.loadmatch.com/images/arrow_black_horz.gif')

    # if found, replace 'Arrow' column data with "right"; otherwise, "left" (left image has different url name)
    if img and len(row_data) >= 3:  # make sure 'Arrow' column exists 
        row_data[2] = 'Right'
    elif len(row_data) >= 3:
        row_data[2] = 'Left'

    # if the row has 14 cells, start scraping - refers to column #
    if len(row_data) == 14:
        start_scraping = True

    # if the row has less than 14 cells, stop scraping
    elif len(row_data) < 14 and start_scraping:
        break

    # if the row has data and scraping has started, append it to column_data
    if row_data and start_scraping:
        column_data.append(row_data)

# define column names
column_names = ['Terminal Name', 'Terminal', 'Arrow', 'Zip Code', 'State', 'Province', 'Seven', 'Eight', 
                'Total', 'Notes', 'One-Way Miles', 'Per Mile (fuel incl)', 'Date','Blank']

# convert scraped data to df
df = pd.DataFrame(column_data, columns=column_names)

# change dir to your file location 
os.chdir('/Users/')

# read prev. version in
prev_df = pd.read_csv('data.csv')

# update any new data to sheet
updated_df = pd.concat([df, prev_df]).drop_duplicates()

# write to csv
updated_df.to_csv('data.csv', index=False)
