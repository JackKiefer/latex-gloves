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

./convert.sh || exit 1

echo "Cleaning up the mess..."
rm pdf/*.aux
rm pdf/*.log

echo "Bringing the Canvas quiz to life..."
python gloves.py
