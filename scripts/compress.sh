#!/bin/bash
timestamp=$(date +%s)
filename="build-${timestamp}.zip"
output_dir="./build"

mkdir -p "$output_dir"

rsync -av --exclude='__pycache__' src/* $output_dir/bundle
rsync requirements.txt $output_dir/bundle

cd $output_dir/bundle

zip -r $filename *

cd ..
cp ./bundle/$filename .

rm -rf bundle

echo "Zip file saved to ${output_dir}/build-${timestamp}.zip"
