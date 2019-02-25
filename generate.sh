#!/bin/bash

if [ $# -eq 0 ]; then
  echo "No input quiz specified"
  exit 1
fi

rm questionData.pickle
rm pdf/*
rm tex/*
rm svg/*

python separate.py $1
