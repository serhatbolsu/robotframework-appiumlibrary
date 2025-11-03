import os
import argparse
import re

KEYWORD_MAP = {
    "text should be visible": ("Expect Text", "visible"),
    "element should be disabled": ("Expect Element", "disabled"),
    "element should be enabled": ("Expect Element", "enabled"),
    "element should be visible": ("Expect Element", "visible"),
    "element value should be": ("Element Attribute Should Match", "value"),
    "element name should be": ("Element Attribute Should Match","name")
}

OPTIONAL_ARGUMENTS = {
    "text should be visible": ["exact_match", "loglevel"],
    "element should be disabled": ["loglevel"],
    "element should be enabled": ["loglevel"],
    "element should be visible": ["loglevel"],
}

FILE_EXTENSIONS = (".robot", ".resource")
SPACES = " " * 4

def migrate_file(file_path: str, dry_run: bool=False) -> bool:
    # Open the file and read all lines
    modified = False
    new_lines = []
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
 
    # For each line, remove leading spaces but preserve the indentation
    for line in lines:
        stripped_line = line.lstrip()
        leading_spaces = line[:len(line) - len(stripped_line)]
        updated_line = line
 
        # loop over the keywords in the map and match the old keyword
        for old_kw, (new_kw, arg_value) in KEYWORD_MAP.items():
            pattern = r'^' + re.escape(old_kw) + r'\s*(.*)$'
            match = re.match(pattern, stripped_line, re.IGNORECASE)

            if not match:
                continue

            
            # if a match is found, then it updates the line
            args = re.split(r'\s{2,}', match.group(1).strip()) # split arguments, consider at least 2 spaces 
            locator = args[0]
            expected = args[1]  if len(args) > 1 else ""

            # Collect optional arguments
            optional_args = {}
            for i, arg_name in enumerate(OPTIONAL_ARGUMENTS.get(old_kw, [])):
                if len(args) > 1 + i:
                    optional_args[arg_name] = args[i + 1]

            # special case: element value should be or element name should be
            if old_kw in ["element value should be", "element name should be"]:
                updated_line = f"{leading_spaces}{new_kw}{SPACES}{locator}{SPACES}{arg_value}{SPACES}{expected}"
            else: # default case: locator followed by arg_value
                updated_line = f"{leading_spaces}{new_kw}{SPACES}{locator}{SPACES}{arg_value}"

            # if extra arguments exist, append them to the end in the order they appear
            for arg_name, arg_value in optional_args.items():
                if optional_args:
                    if arg_name in arg_value:
                        updated_line += f"{SPACES}{arg_value}"
                    else:
                        updated_line += f"{SPACES}{arg_name}={arg_value}"

            updated_line += "\n"

            modified = True
            break
        # Append the updated line
        new_lines.append(updated_line)
 
        if dry_run and updated_line != line:
            print(f"[DRY RUN] Original line: {line}")
            print(f"[DRY RUN] Updated line: {updated_line}\n")

    if modified:
        if dry_run:
            print(f"[DRY RUN] {file_path} would be updated.")
        else:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"[CHANGED] Updated: {file_path}")
    return modified
 
def migrate_repository(root_dir: str, dry_run=False):

    updated_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(FILE_EXTENSIONS):
                full_path = os.path.join(dirpath, filename)
                if migrate_file(full_path, dry_run=dry_run):
                    updated_files.append(full_path)
 
def main():
    parser = argparse.ArgumentParser(description="Migrate old AppiumLibrary keywords.")
    parser.add_argument("path", help="Path to a .robot, a .resource file or a directory")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing files")
    args = parser.parse_args()
 
    if os.path.isfile(args.path) and args.path.lower().endswith(FILE_EXTENSIONS):
        migrate_file(args.path, dry_run=args.dry_run)
    elif os.path.isdir(args.path):
        migrate_repository(args.path, dry_run=args.dry_run)
    else:
        print("Error: path must be a .robot, a .resource file or a directory.")
 
if __name__ == "__main__":

    main()

 