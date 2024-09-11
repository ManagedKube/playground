#!/bin/bash

# Replace "your_file.txt" with the actual filename
file="out.txt"

line_count=0

while read line; do
  line_count=$((line_count + 1))

  echo "$line"

  if (( line_count % 6 == 0 )); then
    echo "-----"
  fi
done < "$file"