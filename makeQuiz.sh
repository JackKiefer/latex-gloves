#!/bin/sh

if [ $# -eq 0 ]; then
  echo "No input quiz specified"
  exit 1
fi

echo "Preparing LaTeX gloves..."

rm questionData.pickle
rm pdf/*
rm tex/*
rm svg/*

python texParser.py $1 || exit 1

echo "Oh, Rocky!"

for f in tex/*.tex
do
  filename=$(echo $f | sed 's/.*\/\(.*\)\.tex/\1/')
  echo "Processing question $filename..."
  pdflatex -output-directory ./pdf/ tex/$filename.tex >/dev/null || exit 1
  pdf2svg pdf/$filename.pdf svg/$filename.svg || exit 1
done

echo "Cleaning up the mess..."
rm pdf/*.aux
rm pdf/*.log

echo "Bringing the Canvas quiz to life..."
python gloves.py
