# Week 25: File System Automation

## Overview
This week begins the Automation Track. You'll learn to automate file system tasks using Python's os, shutil, and pathlib modules.

---

## Part 1: The pathlib Module (Modern Approach)

```python
from pathlib import Path

# Current directory
cwd = Path.cwd()
print(cwd)

# Home directory
home = Path.home()
print(home)

# Create paths
path = Path("/home/user/documents")
path = Path("folder") / "subfolder" / "file.txt"

# Path properties
path = Path("/home/user/documents/report.pdf")
print(path.name)        # report.pdf
print(path.stem)        # report
print(path.suffix)      # .pdf
print(path.parent)      # /home/user/documents
print(path.parts)       # ('/', 'home', 'user', 'documents', 'report.pdf')

# Check existence
path.exists()
path.is_file()
path.is_dir()

# Get file info
path.stat().st_size     # Size in bytes
path.stat().st_mtime    # Modification time
```

---

## Part 2: Directory Operations

```python
from pathlib import Path
import shutil

# Create directories
Path("new_folder").mkdir()
Path("nested/folders/here").mkdir(parents=True, exist_ok=True)

# List directory contents
for item in Path(".").iterdir():
    print(item)

# List specific files
for py_file in Path(".").glob("*.py"):
    print(py_file)

# Recursive glob
for file in Path(".").rglob("*.txt"):
    print(file)

# Delete directory
Path("empty_folder").rmdir()  # Must be empty
shutil.rmtree("folder_with_contents")  # Recursive delete
```

---

## Part 3: File Operations

```python
from pathlib import Path
import shutil

# Read file
content = Path("file.txt").read_text()
bytes_content = Path("file.bin").read_bytes()

# Write file
Path("file.txt").write_text("Hello, World!")
Path("file.bin").write_bytes(b"binary data")

# Copy files
shutil.copy("source.txt", "dest.txt")
shutil.copy2("source.txt", "dest.txt")  # Preserves metadata

# Move/rename files
shutil.move("old.txt", "new.txt")
Path("old.txt").rename("new.txt")

# Delete files
Path("file.txt").unlink()
Path("file.txt").unlink(missing_ok=True)  # No error if missing
```

---

## Part 4: The os Module

```python
import os

# Environment variables
home = os.environ.get("HOME")
path = os.environ.get("PATH")

# Current directory
cwd = os.getcwd()
os.chdir("/path/to/directory")

# List directory
files = os.listdir(".")

# Walk directory tree
for root, dirs, files in os.walk("."):
    print(f"Directory: {root}")
    for file in files:
        print(f"  File: {file}")

# Execute system command
os.system("ls -la")
exit_code = os.system("echo hello")
```

---

## Part 5: File Metadata

```python
from pathlib import Path
from datetime import datetime
import os

path = Path("file.txt")
stats = path.stat()

# Size
size_bytes = stats.st_size
size_kb = stats.st_size / 1024
size_mb = stats.st_size / (1024 * 1024)

# Timestamps
modified = datetime.fromtimestamp(stats.st_mtime)
accessed = datetime.fromtimestamp(stats.st_atime)
created = datetime.fromtimestamp(stats.st_ctime)

print(f"Size: {size_kb:.2f} KB")
print(f"Modified: {modified}")

# Permissions (Unix)
mode = stats.st_mode
is_readable = os.access(path, os.R_OK)
is_writable = os.access(path, os.W_OK)
```

---

## Part 6: Batch File Operations

```python
from pathlib import Path
import shutil

def batch_rename(directory, pattern, replacement):
    """Rename files matching a pattern."""
    path = Path(directory)
    renamed = 0

    for file in path.iterdir():
        if pattern in file.name:
            new_name = file.name.replace(pattern, replacement)
            file.rename(file.parent / new_name)
            renamed += 1
            print(f"Renamed: {file.name} -> {new_name}")

    return renamed

def organize_by_extension(directory):
    """Organize files into folders by extension."""
    path = Path(directory)

    for file in path.iterdir():
        if file.is_file():
            ext = file.suffix.lower() or "no_extension"
            ext_folder = path / ext[1:]  # Remove dot
            ext_folder.mkdir(exist_ok=True)
            shutil.move(str(file), str(ext_folder / file.name))
            print(f"Moved {file.name} to {ext_folder.name}/")

def find_large_files(directory, size_mb=100):
    """Find files larger than specified size."""
    path = Path(directory)
    large_files = []

    for file in path.rglob("*"):
        if file.is_file():
            size = file.stat().st_size / (1024 * 1024)
            if size > size_mb:
                large_files.append((file, size))

    return sorted(large_files, key=lambda x: x[1], reverse=True)

def find_duplicates(directory):
    """Find duplicate files by hash."""
    import hashlib

    path = Path(directory)
    hashes = {}
    duplicates = []

    for file in path.rglob("*"):
        if file.is_file():
            file_hash = hashlib.md5(file.read_bytes()).hexdigest()
            if file_hash in hashes:
                duplicates.append((file, hashes[file_hash]))
            else:
                hashes[file_hash] = file

    return duplicates
```

---

## Part 7: File Watching

```python
import time
from pathlib import Path
from datetime import datetime

def watch_directory(directory, interval=1):
    """Watch directory for changes."""
    path = Path(directory)

    # Get initial state
    previous = {f: f.stat().st_mtime for f in path.iterdir() if f.is_file()}
    print(f"Watching {directory}...")

    try:
        while True:
            time.sleep(interval)
            current = {f: f.stat().st_mtime for f in path.iterdir() if f.is_file()}

            # Check for new files
            new_files = set(current.keys()) - set(previous.keys())
            for f in new_files:
                print(f"[{datetime.now()}] NEW: {f.name}")

            # Check for deleted files
            deleted = set(previous.keys()) - set(current.keys())
            for f in deleted:
                print(f"[{datetime.now()}] DELETED: {f.name}")

            # Check for modified files
            for f in current:
                if f in previous and current[f] != previous[f]:
                    print(f"[{datetime.now()}] MODIFIED: {f.name}")

            previous = current

    except KeyboardInterrupt:
        print("\nStopped watching.")

# Usage
# watch_directory("./my_folder")
```

---

## Part 8: Working with Archives

```python
import shutil
import zipfile
import tarfile
from pathlib import Path

# Create ZIP archive
shutil.make_archive("backup", "zip", "folder_to_backup")

# Extract ZIP
shutil.unpack_archive("backup.zip", "extracted_folder")

# More control with zipfile
with zipfile.ZipFile("archive.zip", "w") as zf:
    for file in Path(".").glob("*.txt"):
        zf.write(file)

# Read ZIP contents
with zipfile.ZipFile("archive.zip", "r") as zf:
    print(zf.namelist())
    zf.extractall("output_folder")

# TAR archives
with tarfile.open("archive.tar.gz", "w:gz") as tf:
    tf.add("folder")

with tarfile.open("archive.tar.gz", "r:gz") as tf:
    tf.extractall("output_folder")
```

---

## Week 25 Project: Downloads Organizer

```python
#!/usr/bin/env python3
"""
Downloads Folder Organizer
Automatically organizes files by type into subfolders.
"""

from pathlib import Path
import shutil
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# File type categories
CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx"],
    "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "Code": [".py", ".js", ".html", ".css", ".java", ".cpp", ".c", ".h", ".json", ".xml"],
    "Executables": [".exe", ".msi", ".dmg", ".app", ".deb", ".rpm"],
    "Fonts": [".ttf", ".otf", ".woff", ".woff2"],
    "Data": [".csv", ".sql", ".db", ".sqlite"],
}

def get_category(file_path: Path) -> str:
    """Get category for a file based on extension."""
    ext = file_path.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "Other"

def organize_downloads(downloads_path: str, dry_run: bool = False):
    """Organize files in downloads folder by type."""
    downloads = Path(downloads_path)

    if not downloads.exists():
        logger.error(f"Directory not found: {downloads}")
        return

    stats = {"moved": 0, "skipped": 0, "errors": 0}

    for file_path in downloads.iterdir():
        # Skip directories and hidden files
        if file_path.is_dir() or file_path.name.startswith("."):
            continue

        category = get_category(file_path)
        category_folder = downloads / category

        try:
            if not dry_run:
                category_folder.mkdir(exist_ok=True)

                # Handle duplicate names
                dest = category_folder / file_path.name
                if dest.exists():
                    stem = file_path.stem
                    suffix = file_path.suffix
                    counter = 1
                    while dest.exists():
                        dest = category_folder / f"{stem}_{counter}{suffix}"
                        counter += 1

                shutil.move(str(file_path), str(dest))
                logger.info(f"Moved: {file_path.name} -> {category}/")
            else:
                logger.info(f"[DRY RUN] Would move: {file_path.name} -> {category}/")

            stats["moved"] += 1

        except Exception as e:
            logger.error(f"Error moving {file_path.name}: {e}")
            stats["errors"] += 1

    logger.info(f"\nSummary: Moved {stats['moved']}, Errors: {stats['errors']}")
    return stats

def cleanup_empty_folders(directory: str):
    """Remove empty folders."""
    path = Path(directory)
    removed = 0

    for folder in path.iterdir():
        if folder.is_dir() and not any(folder.iterdir()):
            folder.rmdir()
            logger.info(f"Removed empty folder: {folder.name}")
            removed += 1

    return removed

def generate_report(directory: str):
    """Generate a report of folder contents."""
    path = Path(directory)
    report = []
    total_size = 0
    total_files = 0

    report.append(f"Report for: {directory}")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 50)

    for folder in sorted(path.iterdir()):
        if folder.is_dir():
            files = list(folder.rglob("*"))
            file_count = len([f for f in files if f.is_file()])
            folder_size = sum(f.stat().st_size for f in files if f.is_file())

            total_files += file_count
            total_size += folder_size

            size_mb = folder_size / (1024 * 1024)
            report.append(f"\n{folder.name}/")
            report.append(f"  Files: {file_count}")
            report.append(f"  Size: {size_mb:.2f} MB")

    report.append("\n" + "=" * 50)
    report.append(f"Total files: {total_files}")
    report.append(f"Total size: {total_size / (1024 * 1024):.2f} MB")

    return "\n".join(report)

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Organize downloads folder")
    parser.add_argument("path", nargs="?", default="~/Downloads",
                       help="Path to organize (default: ~/Downloads)")
    parser.add_argument("--dry-run", action="store_true",
                       help="Show what would be done without moving files")
    parser.add_argument("--report", action="store_true",
                       help="Generate report only")
    parser.add_argument("--cleanup", action="store_true",
                       help="Remove empty folders")

    args = parser.parse_args()

    path = Path(args.path).expanduser()

    if args.report:
        print(generate_report(str(path)))
    elif args.cleanup:
        cleanup_empty_folders(str(path))
    else:
        organize_downloads(str(path), dry_run=args.dry_run)

if __name__ == "__main__":
    main()
```

---

## Key Takeaways

1. **pathlib** is the modern way to handle paths
2. Use **shutil** for high-level file operations
3. **os.walk()** for recursive directory traversal
4. **glob** patterns for file matching
5. Always **handle errors** gracefully
6. Use **dry run** mode for testing
7. **Log operations** for debugging
8. **Backup** before bulk operations

---

## Next Week Preview
Week 26 covers web scraping with requests and BeautifulSoup.
