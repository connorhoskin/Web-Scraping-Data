
from bs4 import BeautifulSoup
import requests
import re
import json

def update_paper_codes(paper_codes):
    if not paper_codes:
        return []
    # Define the base URL for fetching paper codes
    base_url = "https://www.otago.ac.nz/courses/papers?papercode="
    # print(paper_codes)
    paper_codes = list(set(paper_codes))
   # print("___________________")
    #print(paper_codes)
    # Create a copy of the original array to store the updated paper codes
    updated_codes = paper_codes.copy()

    # Iterate over the list of paper codes
    for i, code in enumerate(updated_codes):
        # Check if the code ends with ".*"
        if code.endswith(".*"):
            # Construct the URL for fetching the actual paper codes
            url = base_url + code  # Remove ".*" from the code

            # Make a request to the URL
            response = requests.get(url)

            # Check if the request was successful
            if response.status_code == 200:
                # Parse the response to extract the actual paper codes
                soup = BeautifulSoup(response.text, 'html.parser')

                try:
                    # Try to find the table
                    table = soup.find('table')

                        # Check if the table is found
                    if table is None:
                        raise ValueError("Table not found in the HTML")

                        # Continue with further processing of the table
                        # ...

                except ValueError as e:
                    # Handle the case where the table is not found
                    return []
                tbody = table.find('tbody')

                # Initialize an empty list to store the paper codes
                new_paperCodes = []

                # Iterate through each row in the table body
                for row in tbody.find_all('tr'):
                    # Find the first cell in the row
                    td = row.find('td')

                    # Find the anchor tag within the cell
                    a = td.find('a')

                    # Extract the text content of the anchor tag and append it to the list of paper codes
                    new_paperCodes.append(a.get_text(strip=True))
                # print(table)
                # Extract the actual codes from the soup object

                # Replace the wildcard pattern with the actual paper codes in the list
                updated_codes[i:i + 1] = new_paperCodes



    updated_codes = list(set(updated_codes))
    sorted_paper_codes = sorted(updated_codes)
    #print(sorted_paper_codes)
    return sorted_paper_codes

url = "https://www.otago.ac.nz/courses/qualifications/ba"
response = requests.get(url)
results = {}
# Check if request was successful
if response.status_code == 200:
    page_content = response.text
else:
    print("FUCK U")

soup = BeautifulSoup(page_content, 'html.parser')
requirements_panel = soup.find('div', class_='requirements-panel__container')
# Locate each major div inside the requirements panel
for major_div in requirements_panel.find_all('div', recursive=False)[1:]:
    title_div =  major_div.find_all('div', recursive=False)[0]
    sentence = title_div.find('div').get_text(strip=True)
    major_name = sentence.split(" in ")[-1]

    second_div = major_div.find_all('div', recursive=False)[1]
    table = second_div.find('table')
    results[major_name] = {}


    # Iterate through each row in the table body
    for row in table.find('tbody').find_all('tr')[1:4]:

        # Find the first cell in the row, which contains the level
        level_cell = row.find('td')

        # Check if the level cell is found (to skip header row)
        if level_cell:
            papers =[]
            # Extract the level text
            level = level_cell.get_text(strip=True)

            # Find the second cell in the row, which contains the papers
           # papers_cell = level_cell.find_next_sibling('td')

            # Find all the anchor tags within the papers cell, which contain the paper links and codes
            paper_links = row.find_all('a')
            papers = [link.attrs['href'].split('=')[-1] for link in paper_links if '=' in link.attrs['href']]
            results[major_name][level] = update_paper_codes(papers)
            print(results[major_name][level])
            # Print the level and the corresponding papers
            #print(f"{level}: {updated_paper_codes}")

with open("testMe.json", "w") as outfile:
   json.dump(results, outfile, indent=4)
