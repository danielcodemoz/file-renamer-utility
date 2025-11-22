import os
import sys

def rename_files(directory_path):
    """
    Renames files in the specified directory:
    1. Replaces spaces with underscores.
    2. Converts all characters to lowercase.
    """
    
    # Check if the directory exists
    if not os.path.isdir(directory_path):
        print(f"❌ Error: Directory not found at '{directory_path}'")
        return

    print(f"✨ Starting file renaming in: {directory_path}")
    
    # Counter for renamed files
    renamed_count = 0
    
    try:
        # Loop through all items in the directory
        for filename in os.listdir(directory_path):
            # Construct the full path
            old_filepath = os.path.join(directory_path, filename)
            
            # Skip directories, we only want to process files
            if os.path.isdir(old_filepath):
                continue
            
            # 1. Apply the renaming logic
            new_filename = filename.replace(" ", "_").lower()
            
            # Check if a change actually occurred
            if new_filename != filename:
                new_filepath = os.path.join(directory_path, new_filename)
                
                # Check for potential file name conflict
                if os.path.exists(new_filepath):
                    print(f"⚠️ Warning: Skipping '{filename}'. Destination '{new_filename}' already exists.")
                    continue
                
                # Perform the rename operation
                os.rename(old_filepath, new_filepath)
                print(f"✅ Renamed: '{filename}' -> '{new_filename}'")
                renamed_count += 1
            else:
                # print(f"ℹ️ Skipping: '{filename}' (No changes needed)")
                pass # Silent skip for files that already conform

        print(f"\n🎉 Finished! Total files renamed: {renamed_count}")
        
    except Exception as e:
        print(f"\n🔥 An unexpected error occurred: {e}")

if __name__ == "__main__":
    # The script expects the directory path as a command-line argument
    if len(sys.argv) < 2:
        print("Usage: python file_renamer.py <directory_path>")
        print("\nExample: python file_renamer.py ./Documents/photos")
        sys.exit(1)
        
    target_directory = sys.argv[1]
    rename_files(target_directory)
