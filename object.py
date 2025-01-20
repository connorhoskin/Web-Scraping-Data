import json

# Read paper titles from the first file
with open('recomendedPapers.json', 'r') as f:
    paper_titles_data = json.load(f)

# Read paper objects from the second file
with open('papers.json', 'r') as f:
    paper_objects_data = json.load(f)

# Replace paper titles with corresponding paper objects using the paper code as key
for degree, subjects in paper_titles_data.items():
    for subject, levels in subjects.items():
        for level, papers in levels.items():
            paper_objects_dict = {}
            for paper_title in papers:
                if paper_title in paper_objects_data:
                    paper_objects_dict[paper_title] = paper_objects_data[paper_title]
                else:
                    paper_objects_dict[paper_title] = {"error": f"Paper object for {paper_title} not found"}
            levels[level] = paper_objects_dict

# Write the updated data structure to an output file
with open('output_file.json', 'w') as f:
    json.dump(paper_titles_data, f, indent=2)

print("Done!")
