def remove_duplicate_urls(input_file_path, output_file_path):
    try:
        # Read all lines from the input file
        with open(input_file_path, 'r') as infile:
            lines = infile.readlines()

        # Use a list to maintain the order while removing duplicates
        unique_urls = []
        seen_urls = set()
        for line in lines:
            if line not in seen_urls:
                seen_urls.add(line)
                unique_urls.append(line)

        # Write the unique URLs back to the output file
        with open(output_file_path, 'w') as outfile:
            outfile.writelines(unique_urls)

        print(f"Removed duplicate URLs. The unique URLs have been saved to '{output_file_path}'.")
    except FileNotFoundError:
        print(f"File not found: '{input_file_path}'")
    except Exception as e:
        print(f"An error occurred: {e}")

# Specify the input and output file paths
input_file_path = 'tester.txt'
output_file_path = 'finished.txt'

# Call the function to remove duplicate URLs
remove_duplicate_urls(input_file_path, output_file_path)
