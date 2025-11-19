import os
import argparse
import re
from robot.api.parsing import get_model, ModelVisitor

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

class KeywordMigrator(ModelVisitor):
    def __init__(self, lines, file_path):
        self.lines = lines
        self.file_path = file_path
        self.modified = False

    def visit_KeywordCall(self, node):
        kw_name = node.keyword.lower()
        if kw_name not in KEYWORD_MAP:
            return
        lineno = node.lineno
        line = self.lines[lineno - 1]
        leading_spaces = re.match(r"\s*", line).group(0)

        new_kw, arg_value = KEYWORD_MAP[kw_name]

        args_text = "  ".join(node.args) if hasattr(node, "args") else ""
        args = re.split(r'\s{2,}', args_text.strip()) if args_text else []
        locator = args[0] if len(args) > 0 else ""
        expected = args[1]  if len(args) > 1 else ""

        # Collect optional arguments
        optional_args = {}
        for i, arg_name in enumerate(OPTIONAL_ARGUMENTS.get(kw_name, [])):
            if len(args) > 1 + i:
                optional_args[arg_name] = args[i + 1]

        # special case: element value should be or element name should be
        if kw_name in ["element value should be", "element name should be"]:
            updated_line = f"{leading_spaces}{new_kw}{SPACES}{locator}{SPACES}{arg_value}{SPACES}{expected}"
        else: # default case: locator followed by arg_value
            updated_line = f"{leading_spaces}{new_kw}{SPACES}{locator}{SPACES}{arg_value}"

        # if extra arguments exist, append them to the end in the order they appear
        for arg_name, arg_value in optional_args.items():
            if arg_name in arg_value:
                updated_line += f"{SPACES}{arg_value}"
            else:
                updated_line += f"{SPACES}{arg_name}={arg_value}"

        updated_line += "\n"

        # log changes
        print(f"[UPDATE] {self.file_path}: {lineno}")
        print(f" From: {line.strip()}")
        print(f" To:   {updated_line.strip()}\n")

        self.lines[lineno - 1] = updated_line
        self.modified = True

def migrate_file(file_path: str, dry_run=False) -> bool:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        model = get_model(file_path)
    except Exception as e:
        print(f"[ERROR] {e}, could not parse {file_path}!")
        return False
    
    migrator = KeywordMigrator(lines, file_path)
    migrator.visit(model)

    if migrator.modified:
        if dry_run:
            print(f"[DRY RUN] {file_path} would be updated.\n")
        else:
            with open(file_path, "w", encoding="utf-8") as f:
                f.writelines(lines)
            print(f"[CHANGED] Updated: {file_path}\n")
    return migrator.modified

def migrate_repository(root_dir: str, dry_run:bool=False):
    updated_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(FILE_EXTENSIONS):
                full_path = os.path.join(dirpath, filename)
                if migrate_file(full_path, dry_run):
                    updated_files.append(full_path)
    if not updated_files:
        print(f"No matching keywords founds in {root_dir}")


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

 