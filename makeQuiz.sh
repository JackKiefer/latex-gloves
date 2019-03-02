#!/bin/bash

if [ $# -eq 0 ]; then
  echo "No input quiz specified"
  exit 1
fi

echo "Preparing LaTeX gloves..."

rm questionData.pickle
rm pdf/*
rm tex/*
rm svg/*

python separate.py $1

echo "Oh, Rocky!"

for f in tex/*.tex
do
  filename=$(echo $f | sed 's/.*\/\(.*\)\.tex/\1/')
  echo "Processing question $filename..."
  pdflatex -output-directory ./pdf/ tex/$filename.tex >/dev/null
  pdf2svg pdf/$filename.pdf svg/$filename.svg
done

echo "Cleaning up the mess..."
rm pdf/*.aux
rm pdf/*.log

echo "Bringing the Canvas quiz to life..."
#python gloves.py
