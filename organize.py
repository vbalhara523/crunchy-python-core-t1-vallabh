import argparse
from pathlib import Path
import shutil
import sys

def setup_arguments():
    """Parses command-line arguments for the script."""
    parser = argparse.ArgumentParser(description="Organize files in a directory by extension.")
    parser.add_argument("target_dir", type=str, help="Relative path to the directory to organize.")
    parser.add_argument("--dry-run", action="store_true", help="Simulate the organization without moving files.")
    return parser.parse_args()

def get_file_category(file_extension):
    """Determines the category folder name based on the file extension."""
    extensions_map = {
        ".jpg": "Images", ".png": "Images", ".jpeg": "Images",
        ".pdf": "Documents", ".txt": "Documents", ".csv": "Documents",
        ".mp4": "Videos", ".mp3": "Audio",
        ".zip": "Archives", ".tar": "Archives"
    }
    return extensions_map.get(file_extension.lower(), "Others")

def move_file(file_path, target_folder, dry_run):
    """Moves a file to the target folder, handling existing files and dry runs."""
    target_folder.mkdir(parents=True, exist_ok=True)
    destination = target_folder / file_path.name
    
    if destination.exists():
        print(f"Skip: {file_path.name} already exists in {target_folder.name}")
        return

    if dry_run:
        print(f"[DRY RUN] Would move {file_path.name} to {target_folder.name}/")
    else:
        shutil.move(file_path, destination)
        print(f"Moved {file_path.name} to {target_folder.name}/")

def organize_directory(directory_path, dry_run):
    """Iterates through a directory and organizes files into categorized subfolders."""
    if not directory_path.exists() or not directory_path.is_dir():
        print(f"Error: Directory '{directory_path}' does not exist or is not a directory.")
        sys.exit(1)

    for item in directory_path.iterdir():
        if item.is_file():
            category = get_file_category(item.suffix)
            target_folder = directory_path / category
            move_file(item, target_folder, dry_run)

def main():
    """Main execution entry point."""
    args = setup_arguments()
    target_dir = Path(args.target_dir)
    organize_directory(target_dir, args.dry_run)

if __name__ == "__main__":
    main()
