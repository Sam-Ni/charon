import os
import argparse

def main():
    parser = argparse.ArgumentParser(description='Collect all submodules and types in the Rust std documentation.')
    parser.add_argument('dir_path', help='Root directory of the Rust std documentation (required)')  # Added positional argument
    parser.add_argument('--ignore', action='append', default=[],
                        help='Directory names to ignore (can be used multiple times), e.g., --ignore=os --ignore=fs')
    parser.add_argument('--flat-modules', action='append', default=[],
                        help='Specify module paths (e.g., collections or collections/hash_map); subdirectories under these modules will not be recursively traversed (but the module itself and its direct files will still be output)')
    args = parser.parse_args()

    ignore_dirs = set(args.ignore)  # Globally ignored directory names (any directory with the same name at any level will be skipped)
    # Convert paths in flat_modules to system separators and normalize them
    flat_modules = {os.path.normpath(p) for p in args.flat_modules}

    output_file = "std_modules.txt"
    current_dir = args.dir_path + '/share/doc/rust/html/std'  # Use the directory specified by the command-line argument

    # Optional: check if the directory exists
    if not os.path.isdir(current_dir):
        print(f"Error: directory '{current_dir}' does not exist or is not a directory")
        return

    with open(output_file, "w", encoding="utf-8") as f:
        # Recursively traverse all subdirectories and sort subdirectory names to ensure order
        for root, dirs, files in os.walk(current_dir, topdown=True):
            # Sort subdirectories in the current directory for lexicographic traversal order
            dirs.sort()
            # Filter out globally ignored directories
            dirs[:] = [d for d in dirs if d not in ignore_dirs]

            # Compute relative path and skip the root directory itself
            rel_path = os.path.relpath(root, current_dir)
            if rel_path == ".":
                continue

            # If the current module is in flat_modules, prevent further recursion into its subdirectories
            if rel_path in flat_modules:
                dirs[:] = []  # Clear the subdirectory list to stop further traversal

            # Build module prefix: std::module1::module2...
            components = rel_path.split(os.sep)
            module_prefix = "std::" + "::".join(components)

            # Output the module itself
            f.write(f"{module_prefix}::*\n")

            # Sort .html files in the current directory to ensure output order
            files.sort()
            for file in files:
                if not file.endswith(".html"):
                    continue

                # Check if the filename starts with one of the specified prefixes
                for prefix in ("struct.", "enum.", "union."):
                    if file.startswith(prefix):
                        # Extract the type name: remove the prefix and .html suffix
                        type_name = file[len(prefix):-5]  # Remove ".html" (5 characters)
                        # Output the type
                        f.write(f"{module_prefix}::{type_name}::*\n")
                        break  # Only one prefix matches per file

if __name__ == "__main__":
    main()