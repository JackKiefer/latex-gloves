#!/bin/sh

# Convert all .tex files in tex/ to svg images in svg/

for f in tex/*.tex
do
  filename=$(echo $f | sed 's/.*\/\(.*\)\.tex/\1/')
  echo "Processing question $filename..."
  pdflatex -output-directory ./pdf/ tex/$filename.tex >/dev/null || exit 1
  pdf2svg pdf/$filename.pdf svg/$filename.svg || exit 1
done
