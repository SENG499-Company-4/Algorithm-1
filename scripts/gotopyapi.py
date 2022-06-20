"""Converts Go Struct Defs to Pydantic BaseModels"""

import re
import sys

NAME_PATTERN = r"type (?P<name>[A-Za-z0-9_]+) struct \{"
FIELD_PATTERN = r"[ \t]+[A-Za-z0-9_]+[ \t]+(?P<type>[A-Za-z0-9_\[\]]+)[ \t]+`json:\"(?P<name>[A-Za-z-_]+)(,omitempty)?\"`"

CLASS_TEMPLATE = "\nclass {name}(BaseModel):"
FIELD_TEMPLATE = "    {name}: {type}"


def main():
    with open(sys.argv[1]) as lines:
        py = "\n".join(filter(bool, map(processed_line, lines)))
    
    print(py)


def processed_line(line):
    """Processes a line of Go code into equivalent Python code"""

    if (matches := re.match(NAME_PATTERN, line)) and matches.group("name"):
        return CLASS_TEMPLATE.format(name=matches.group("name"))
    
    if (matches := re.match(FIELD_PATTERN, line)) and matches.group("type") and matches.group("name"):
        return FIELD_TEMPLATE.format(name=matches.group("name"),
                                     type=py_type(matches.group("type")))

    # Remove unknown lines (will be filtered out)
    return ""


def py_type(go_type):
    """Takes a Go type and returns an equivalent Python type"""

    if go_type[:2] == "[]":
        return f"list[{py_type(go_type[2:])}]"

    if go_type == "uint":
        return "int"

    if go_type == "string":
        return "str"

    if go_type == "float32":
        return "float"
    
    return go_type


if __name__ == "__main__":
    main()
