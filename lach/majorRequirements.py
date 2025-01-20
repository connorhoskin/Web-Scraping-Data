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
def is_n_of(n_of):
    if n_of == "one" or n_of == "two" or n_of == "three" or n_of == "four" or n_of == "five" or n_of == "six":
        return True
    return False

for major_div in requirements_panel.find_all('div', recursive=False)[1:]:
    title_div = major_div.find_all('div', recursive=False)[0]
    sentence = title_div.find('div').get_text(strip=True)
    major_name = sentence.split(" in ")[-1]
    second_div = major_div.find_all('div', recursive=False)[1]
    table = second_div.find('table')
    results[major_name] = {}

    # Iterate through each row in the table body
    # Iterate through each row in the table body
    for row in table.find('tbody').find_all('tr')[1:4]:
        # Find the first cell in the row, which contains the level
        level_cell = row.find('td')

        # Check if the level cell is found (to skip header row)
        if level_cell:
            papers = []

            # Extract the level text
            level = level_cell.get_text(strip=True)

            # Check if the major_name key exists in the dictionary, if not, create it
            if major_name not in results:
                results[major_name] = {"levels": {}}

            # Check if the "levels" key exists in the major's dictionary, if not, create it
            if "levels" not in results[major_name]:
                results[major_name]["levels"] = {}

            # Check if the level key exists in the levels dictionary, if not, create it
            if level not in results[major_name]["levels"]:
                results[major_name]["levels"][level] = {}

            # Find the next <td> element after level_cell
            papers_cell = level_cell.find_next_sibling('td')

            if papers_cell:
                paragraphs = papers_cell.find_all('p')
                if paragraphs:
                    for p in paragraphs:
                        # Extract the first word
                        papers_text = p.get_text()
                        first_word = papers_text.split()[0].lower()

                        # Check if it is a number
                        if is_n_of(first_word):
                            n_of_str = first_word + "_of_papers"
                            papers = {}

                            paper_links = row.find_all('a')
                            # Extract the text content of the anchor tags and store in a list
                            papers = [link.attrs['href'].split('=')[-1] for link in paper_links if
                                      '=' in link.attrs['href']]

                            results[major_name]["levels"][level][n_of_str] = update_paper_codes(papers)

                        # Else, if first word is an anchor
                        else:
                            # Check if the first element in p is a paper link
                            paper_link = p.find('a')
                            if paper_link:
                                # Ensure "compulsory_papers" exists in the dictionary
                                if "compulsory_papers" not in results[major_name]["levels"][level]:
                                    results[major_name]["levels"][level]["compulsory_papers"] = []

                                # Append the anchors to the existing "compulsory_papers" list
                                results[major_name]["levels"][level]["compulsory_papers"].append(
                                    paper_link.get_text(strip=True))

                # if td contains no paragraphs (i.e., there is one row of text)
                else:
                    papers_text = papers_cell.get_text()
                    first_word = papers_text.split()[0].lower()

                    # if first word is a number
                    if is_n_of(first_word):
                        n_of_str = first_word + "_of_papers"
                        papers = {}

                        # Check if paragraph contains '-level' anchor to a list of papers
                        if '-level' in papers_text:
                            paper_links = row.find_all('a')
                            papers = [link.attrs['href'].split('=')[-1] for link in paper_links if
                                      '=' in link.attrs['href']]

                        else:
                            # Extract the text content of the anchor tags and store in a list
                            papers = [anchor.get_text(strip=True) for anchor in p.find_all('a') if
                                      '-level' not in anchor.get_text(strip=True)]

                        results[major_name]["levels"][level][n_of_str] = update_paper_codes(papers)

                    # Else, if first word is an anchor
                    else:
                        # Check if the first element in p is an anchor
                        paper = papers_text.find('a')

                        if paper:
                            # Ensure "compulsory_papers" exists in the dictionary
                            if "compulsory_papers" not in results[major_name]["levels"][level]:
                                results[major_name]["levels"][level]["compulsory_papers"] = []

                            # Append the anchors to the existing "compulsory_papers" list
                            results[major_name]["levels"][level]["compulsory_papers"].append(paper.get_text(strip=True))

        # Find the next <tr> element after the current row
        next_row = row.find_next_sibling('tr')
        plus = next_row.find('td')
        if plus:
            if "Plus" in plus:
                paragraph = next_row.find('p')
                if paragraph:
                    plus_text = paragraph.get_text()
                    # Use regular expression to find the first set of digits in the paragraph
                    matches = re.findall(r'\d+', plus_text)
                    # Convert each match to an integer and add it to the points list
                    points = [int(match) for match in matches]
                    # Check if the next_row exists before attempting to process it
                    if len(points) == 3:
                        results[major_name]["further_points"] = points[0]
                        results[major_name]["points_at_" + str(points[2]) + "-level"] = points[1]
                    else:
                        results[major_name]["further_points"] = points[0]


with open("majorRequirements.json", "w") as outfile:
   json.dump(results, outfile, indent=4)
