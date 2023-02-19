import sys
import argparse
import os
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_folder", help="Path to the original tags folder", required=True)
parser.add_argument("-o", "--output_folder", help="Path to the new tags folder", required=True)
args = parser.parse_args()

# sys.argv = args

original_tags_dir = Path(args.input_folder)
new_tags_dir = Path(args.output_folder)

if not os.path.exists(new_tags_dir):
    os.mkdir(new_tags_dir)

for file in os.listdir(original_tags_dir):
    if not file.endswith('.txt'):
        print(f"[INFO] {file} is not a text file, skipping.")
        continue
    with open(f"{original_tags_dir}/{file}", 'rb') as f:
        lines = f.readlines()
        found_tags = []
        # don't add multiple creator tags (if there are) to the beginning of the file due to weight
        creator_found = False
        characters_idx = 1
        for line in lines:
            tag = line.strip().decode('utf-8')

            # ignore these tags
            # TODO: improve list
            bad_tags = ['tagme', 'junk tag', 'meta:anonymous']
            if any(tag == t for t in bad_tags):
                continue

            if '_' in tag:
                tag = tag.replace('_', ' ')

            # only add one creator tag due to frequent dupes from Hydrus
            elif 'creator:' in tag and not creator_found:
                # found_tags.append(tag)
                found_tags.insert(0, tag.split(':')[1]) # remove the namespace add the artist to idx 0
                creator_found = True

            # dupe tags can happen with underscores so don't add dupe tags
            elif ('character:' in tag) and (tag != 'character:original') and tag.split(':')[1] not in found_tags:
                # insert characters to list after artist and increment
                found_tags.insert(characters_idx, tag.split(':')[1])
                characters_idx += 1

            # get namespaced hydrus clothing tags and remove the namespace
            elif 'clothing:' in tag:
                found_tags.append(tag.split(':')[1])

            # get rid of remaining namespaced tags except creator/character and only numeric tags
            elif ':' not in tag and not tag.isnumeric() and tag.isascii():  # and not tag.isnumeric()
                found_tags.append(tag)

        unique_tags = (list(dict.fromkeys(found_tags)))
        with open(f"{new_tags_dir}/{file.split('.')[0]}.txt", 'w', encoding='utf-8') as new_tag_file:
            new_tag_file.write((', '.join(t for t in unique_tags)))
            print(f"[SUCCESS] Updating tags for file: {file.split('.')[0]}.txt")
