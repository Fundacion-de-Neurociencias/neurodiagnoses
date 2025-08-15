#!/bin/bash
set -e

MANIFEST_FILE="data/ingested_knowledge/sources.csv"

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <url> <type>"
    echo "Example: $0 https://example.com/paper.pdf pdf"
    exit 1
fi

URL="$1"
TYPE="$2"
STATUS="pending"
ADDED_ON="2025-08-15"
PROCESSED_ON=""
NOTES=""

# Check if the URL already exists to avoid duplicates
if grep -q "^"*${URL}"*," "$MANIFEST_FILE"; then
    echo "WARNING: URL '$URL' already exists in the manifest. Skipping."
    exit 0
fi

echo "INFO: Adding new source to manifest: $URL"
echo ""$URL","$TYPE","$STATUS","$ADDED_ON","$PROCESSED_ON","$NOTES"" >> "$MANIFEST_FILE"
echo "SUCCESS: Source added."
