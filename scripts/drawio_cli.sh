#!/bin/bash

# Specify format: xml, html, pdf, svg, png
format="$1"

# Specify where to output the file
out_path="$2"

# Specify the file to be converted
in_path="$3"

# Convert the file and capture error logs
drawio --export --format $format --output $out_path $in_path > <"file path goes here"> 2>&1

# confirm
echo conversion complete!

