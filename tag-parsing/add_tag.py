"""
add_tag.py
Purpose: Multi-Character Models / Appending identifier tags
Description: Replace/prepend the first tag and do not replace any desired tags, but prepend the new tag
Usage: python add_tag.py -i "dir/" -o "dir2/" --add_tag "tagname" --keep_tags "tag1 tag2 tag3"
"""

import argparse
import os

parser = argparse.ArgumentParser(description='Replace/prepend the first word in a comma separated text file.')
parser.add_argument('-i', '--input_dir', required=True, help='input directory')
parser.add_argument('-o', '--output_dir', required=True, help='output directory')
parser.add_argument('--add_tag', required=True, help='new tag to replace/prepend to first tag')
parser.add_argument('--keep_tags', nargs='+', default=[], help='comma separated list of tags to keep that may be in the first tag spot to keep')
args = parser.parse_args()

for filename in os.listdir(args.input_dir):
    if not filename.endswith('.txt'):
        continue
    input_path = os.path.join(args.input_dir, filename)
    output_path = os.path.join(args.output_dir, filename)
    with open(input_path, 'r') as in_file, open(output_path, 'w') as out_file:
        for line in in_file:
            tags = line.strip().split(',')
            if tags[0] not in args.keep_tags:
                tags[0] = args.add_tag
            out_file.write(','.join(tags) + '\n')
