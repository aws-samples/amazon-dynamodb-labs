#!/bin/bash

usage() {
    echo "Usage: $0 [--dry-run] -d DEST_REPO"
    echo "  --dry-run    Show what would be synced without making changes"
    echo "  -d, --dest   Destination repository path"
    echo
    echo "Example:"
    echo "  $0 --dry-run -d /Users/$USER/workspace/amazon-dynamodb-immersion-day"
    exit 1
}

# Get the directory where the script is located
SOURCE_REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Parse command line arguments
DRY_RUN=false
DEST_REPO=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        -d|--dest)
            DEST_REPO="$2"
            shift 2
            ;;
        *)
            usage
            ;;
    esac
done

# Validate required parameters
if [ -z "$DEST_REPO" ]; then
    usage
fi

# Define source and destination directory pairs
src_dirs=(
    "content"
    "static"
)

dest_dirs=(
    "content"
    "static"
)

# Define source and destination file pairs
src_files=(
    "design-patterns/cloudformation/vscode.yaml"
)

dest_files=(
    "static/ddb.yaml"
)

# Function to perform sync
perform_sync() {
    local rsync_options="-avz"

    if [ "$DRY_RUN" = true ]; then
        rsync_options="$rsync_options --dry-run"
        echo "Performing dry run..."
    else
        echo "Performing actual sync..."
    fi

    echo "Source repository: $SOURCE_REPO"
    echo "Destination repository: $DEST_REPO"

    # Sync directories
    for i in "${!src_dirs[@]}"; do
        echo "Syncing directory: ${src_dirs[$i]}/ -> ${dest_dirs[$i]}/"
        mkdir -p "$DEST_REPO/${dest_dirs[$i]}"
        rsync $rsync_options "$SOURCE_REPO/${src_dirs[$i]}/" "$DEST_REPO/${dest_dirs[$i]}/"
    done

    # Sync individual files
    for i in "${!src_files[@]}"; do
        echo "Syncing file: ${src_files[$i]} -> ${dest_files[$i]}"
        dest_dir=$(dirname "$DEST_REPO/${dest_files[$i]}")
        mkdir -p "$dest_dir"
        rsync $rsync_options "$SOURCE_REPO/${src_files[$i]}" "$DEST_REPO/${dest_files[$i]}"
    done
    echo "Great! Now follow instructions in the amazon-dynamodb-immersion-day README.md document to complete the sync."
}

# Verify destination repository exists
if [ ! -d "$DEST_REPO" ]; then
    echo "Error: Destination repository does not exist: $DEST_REPO"
    exit 1
fi

# Execute sync
if [ "$DRY_RUN" = true ]; then
    perform_sync
else
    read -p "This will perform an actual sync. Are you sure? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        perform_sync
    else
        echo "Sync cancelled."
        exit 1
    fi
fi
