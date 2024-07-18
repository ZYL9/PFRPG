#!/bin/bash

# Base directory to search for HTML files
base_dir="./docs"

# Find all .md files and loop through each
find "$base_dir" -type f -name "*.md" | while read -r file; do
    # Get the directory and file name without extension
    dir=$(dirname "$file")
    base_name=$(basename "$file" .md)

    # Create the corresponding directory for the output markdown file
    output_dir="./output/$dir"
    mkdir -p "$output_dir"

    enconv -x utf-8 -L none "$file"

    # Define the output file path
    output_file="$output_dir/$base_name.html"

    # Convert Markdown to HTML using pandoc
    pandoc -f markdown -t html "$file" -o "$output_file"

    iconv -f utf-8 -t GBK -c "$output_file" >"$output_file.gbk"

    mv "$output_file.gbk" "$output_file"

done
