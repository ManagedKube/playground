#!/bin/bash

# Replace "your_file.txt" with the actual filename
file="out.txt"

line_count=0

one_line=""

while read line; do
  line_count=$((line_count + 1))

#   echo "$line"
  one_line="$one_line,$line"

  if (( line_count % 6 == 0 )); then
    echo $one_line
    one_line=""
  fi
done < "$file"