#!/bin/bash
filename="app.zip"
output_dir="./build"

mkdir -p "$output_dir"

rsync -av --exclude='__pycache__' src/* $output_dir
rsync requirements.txt $output_dir

cd $output_dir

zip -r $filename *

cd ..
cp $output_dir/$filename .

rm -rf $output_dir

echo "Zip file saved to app.zip"
