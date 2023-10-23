#!/bin/bash

for n in *.ipynb; do
  echo "Processing ${n}..."
  jupyter nbconvert $n --to notebook --execute --inplace
done
