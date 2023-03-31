import argparse
import os
from collections import defaultdict

parser = argparse.ArgumentParser(description='Get the tag frequency in numerical order and write to a file.')
parser.add_argument('-i', '--input_dir', required=True, help='tag input directory')
args = parser.parse_args()

counts = defaultdict(int)
filecount = 0
for file_name in os.listdir(args.input_dir):
    if file_name.endswith('.txt'):
        with open(os.path.join(args.input_dir, file_name), encoding="utf8") as f:
            filecount += 1
            first_line = f.readline().strip()
            items = first_line.split(',')
            # Iterate through the items and update the counts, starting at the second item
            for item in items[1:]:
                counts[item] += 1

# Sort the counts in descending order of frequency (count and percentage) save and print the results
with open('found_tags.txt', 'w', encoding='utf-8') as tag_file:
    for item, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
        image_count = f'{item}: {count}'
        tag_file.write(image_count)
        image_percent = f' - {((count / filecount) * 100):.2f}%'
        tag_file.write(f"{image_percent}\n")
        print(image_count + image_percent)
