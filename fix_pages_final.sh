#!/bin/bash
# Gemini Script for the definitive fix: sanitizing filenames and updating references.
set -e

echo "--> STEP 1: Navigating into the '/docs' directory..."
cd docs

echo "--> STEP 2: Renaming problematic image files..."
# The files have already been renamed by a previous successful run.
# We are skipping the mv commands here.

echo -e "\n--> STEP 3: Updating all HTML files to use the new image names..."
# This command finds and replaces the old names with the new ones in all .html files.
# The use of different delimiters (#) helps handle the complex filenames.
sed -i 's#DALL\·E 2025-02-13 18.19.22 - A collection of four independent, modern images representing key aspects of neuroinformatics___1. __Brain Data Processing__ - A stylized brain w.webp#dalle-neuroinformatics.webp#g' *.html
sed -i 's#multimodal data.webp#multimodal-data.webp#g' *.html
echo "--> HTML files updated."

echo -e "\n--> STEP 4: Navigating back to the project root..."
cd ..

echo -e "\n--> STEP 5: Committing and pushing the definitive fix..."
git add .
git commit -m "fix(pages): Sanitize image filenames and update HTML references" -m "
- Renamed image files with special characters, spaces, and long names to simple, web-safe names.
- Updated all HTML files to point to the new, sanitized image filenames.
- This is the definitive fix for the GitHub Pages deployment workflow, which was failing due to problematic file paths.
"
git push

echo -e "\n========================================================================"
echo "=== ¡REPARACIÓN DEFINITIVA APLICADA! El arreglo ha sido subido. ==="
