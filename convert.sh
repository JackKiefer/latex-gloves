#!/bin/bash

if [ $# -eq 0 ]; then
  echo "No input quiz specified"
  exit 1
fi

rm pdf/*
rm tex/*
rm svg/*

python separate.py $1

for f in tex/*.tex
do
  filename=$(echo $f | sed 's/.*\/\(.*\)\.tex/\1/')
  echo "Processing question $filename..."
  echo "Converting from TeX to PDF..."
  pdflatex -output-directory ./pdf/ tex/$filename.tex >/dev/null
  echo "Converting from PDF to SVG..."
  pdf2svg pdf/$filename.pdf svg/$filename.svg
done

echo "Cleaning up..."
rm pdf/*.aux
rm pdf/*.log

