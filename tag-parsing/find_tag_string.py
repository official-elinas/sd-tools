import os


def search_string(folder, search_term):
    # Iterate through all the files in the folder
    for filename in os.listdir(folder):
        # Check if the file is a text file
        if filename.endswith(".txt"):
            # Open the file and search for the search term
            with open(os.path.join(folder, filename), 'r') as f:
                for line in f:
                    if search_term in line:
                        print(f"Found {search_term} in {filename}")


if __name__ == "__main__":
    search_string("dir", "string_to_search")
