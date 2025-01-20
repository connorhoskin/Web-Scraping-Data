import json

# Read paper titles from the first file
with open('recomendedPapers.json', 'r') as f:
    paper_titles_data = json.load(f)

# Collect all paper titles into a list
paper_titles = []
for degree, subjects in paper_titles_data.items():
    for subject, levels in subjects.items():
        for papers in levels.values():
            paper_titles.extend(papers)

print(paper_titles)
# Read paper objects from the second file
with open('papers.json', 'r') as f:
    paper_objects_data = json.load(f)

# Fetch the paper objects corresponding to the paper titles
fetched_paper_objects = {}
for paper_title in paper_titles:
    if paper_title in paper_objects_data:
        fetched_paper_objects[paper_title] = paper_objects_data[paper_title]

# Write the fetched paper objects to an output file
with open('output_file.json', 'w') as f:
    json.dump(fetched_paper_objects, f, indent=2)

print("Done!")
