# 📁 Simple File Renamer Utility

A command-line Python script designed to clean up file names in a directory.

This utility standardizes filenames by performing two main operations:
1.  **Space to Underscore:** Replaces all spaces (` `) with underscores (`_`).
2.  **Lowercase Conversion:** Converts all characters in the filename to lowercase.

---

## ⚙️ How to Run

### Prerequisites

You need **Python 3.x** installed on your system.

### Usage

1.  **Save the Script:** Save the code above as `file_renamer.py`.
2.  **Run from Terminal:** Execute the script using Python, passing the path to the target directory as the first argument.

```bash
# Example usage:
# The path can be absolute or relative.
python file_renamer.py "/Users/daniel/Desktop/My Files with Spaces"

# Or, for a folder in the current directory:
python file_renamer.py ./test_folder
