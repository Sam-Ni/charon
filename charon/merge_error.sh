#!/bin/bash

# Set directory: use current directory if no parameter provided
target_dir="./std"

# Check if directory exists
if [ ! -d "$target_dir" ]; then
    echo "Error: Directory '$target_dir' does not exist." >&2
    exit 1
fi

# Output file path
output_file="./all_errors.txt"

# Find all files matching *_error.txt, excluding std_error.txt
# Use -print0 and xargs -0 to safely handle special characters in filenames
find "$target_dir" -maxdepth 1 -type f -name "*_error.txt" ! -name "std_error.txt" -print0 | \
    sort -z | \
    xargs -0 -r cat > "$output_file"

# Check if merge was successful
if [ $? -eq 0 ]; then
    echo "Successfully merged all error files (excluding std_error.txt) into: $output_file"
else
    echo "An error occurred during merging." >&2
    exit 1
fi