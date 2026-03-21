#!/bin/bash
# Script to add custom rules to Clash Verge Merge profile

# Define source and destination
SRC="clash_rules.yaml"
DEST="/Users/liuwei/Library/Application Support/io.github.clash-verge-rev.clash-verge-rev/profiles/m4pkI4goLi6q.yaml"

# Check if destination exists
if [ -f "$DEST" ]; then
    echo "Updating existing profile: $DEST"
    cat "$SRC" > "$DEST"
    echo "Successfully updated Clash Verge rules."
else
    echo "Destination profile not found at $DEST"
    echo "Please check your Clash Verge profile settings."
    exit 1
fi
