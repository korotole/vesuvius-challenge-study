#! /bin/bash

# sometimes wget gets stuck, do in a cycle until success
while true; do
    wget --recursive --no-parent -T 15 -c https://dl.ash2txt.org/full-scrolls/Scroll5/PHerc172.volpkg/thaumato_outputs/scroll5_thaumato_jan15/ --accept "composite.jpg" && break
done

BASE_URL="https://dl.ash2txt.org/full-scrolls/Scroll5/PHerc172.volpkg/thaumato_outputs/scroll5_thaumato_jan15"
PREDICTIONS_URL="$BASE_URL/predictions"
LOCAL_BASE_DIR="./dl.ash2txt.org/full-scrolls/Scroll5/PHerc172.volpkg/thaumato_outputs/scroll5_thaumato_jan15"

# Create necessary directories
mkdir -p "$LOCAL_BASE_DIR/predictions"

# Function to download file with retry
download_with_retry() {
    local url=$1
    local output=$2
    local max_attempts=3
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        echo "Downloading $url (attempt $attempt/$max_attempts)"
        if wget -T 30 --show-progress "$url" -O "$output"; then
            return 0
        fi
        
        attempt=$((attempt + 1))
        sleep 2
    done
    
    echo "Failed to download $url after $max_attempts attempts"
    return 1
}

# First, download list of png files from predictions directory
echo "Retrieving list of prediction files..."
wget --spider --force-html -r --no-parent -l 1 --accept "*.png" "$PREDICTIONS_URL" 2>&1 | grep "\.png" | grep -o 'http[s]\?://[^[:space:]]\+' > prediction_files.txt

if [ ! -s prediction_files.txt ]; then
    echo "Failed to retrieve prediction files list. Trying alternative method..."
    wget -q -O- "$PREDICTIONS_URL" | grep -o 'href="[^"]*\.png"' | sed 's/href="//;s/"$//' > prediction_files.txt
fi

echo "Processing prediction files..."
while read -r file_path; do
    # Extract just the filename from the URL or path
    filename=$(basename "$file_path")
    
    # Extract folder name from prediction filename
    # Pattern: working_mesh_0_window_XXXXX_YYYYY_flatboi(_Z)?_prediction_rotated_0_layer_17.png
    if [[ $filename =~ (working_mesh_[0-9]+_window_[0-9]+_[0-9]+_flatboi(_[0-9]+)?)_prediction ]]; then
        folder_name="${BASH_REMATCH[1]}"
        echo "Extracted folder name: $folder_name"
        
        # Create target directory if it doesn't exist
        target_dir="$LOCAL_BASE_DIR/working/$folder_name"
        mkdir -p "$target_dir"
        
        # Download prediction file
        prediction_url="$PREDICTIONS_URL/$filename"
        prediction_output="$target_dir/prediction.png"
        
        echo "Downloading prediction file to $prediction_output"
        download_with_retry "$prediction_url" "$prediction_output"
    else
        echo "Could not parse folder name from: $filename"
        # Download to predictions directory as fallback
        download_with_retry "$PREDICTIONS_URL/$filename" "$LOCAL_BASE_DIR/predictions/$filename"
    fi
done < prediction_files.txt

# Clean up
rm -f prediction_files.txt

echo "Download process completed!"

START_DIR="."

echo "Searching for 'layers' subdirectories starting from $START_DIR..."

# Find all directories named "layers" and remove them
find "$START_DIR" -type d -name "layers" | while read -r dir; do
    echo "Removing directory: $dir"
    rm -rf "$dir"
done

echo "All 'layers' subdirectories have been removed."