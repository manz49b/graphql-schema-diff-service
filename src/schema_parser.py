import re
from typing import Dict, Any

class SchemaParser:
    """A class to parse GraphQL schemas from .txt files into a structured dictionary format."""
    
    # Compile regex patterns for improved performance
    TYPE_REGEX = re.compile(r"type (\w+) {")
    FIELD_WITH_PARAMS_REGEX = re.compile(r"\s*(\w+)\((.*?)\): ([\w\[\]!]+)")
    SIMPLE_FIELD_REGEX = re.compile(r"\s*(\w+): ([\w\[\]!]+)")

    def __init__(self, file_path: str):
        """Initialize the SchemaParser with the path to the schema file."""
        self.file_path = file_path
        self.schema_dict = {}

    def parse_parameters(self, parameters: str) -> Dict[str, str]:
        """Parse input parameters from a field declaration into a dictionary."""
        if not parameters:
            return {}
        return {
            param.split(": ")[0]: param.split(": ")[1] 
            for param in parameters.split(", ")
        }

    def parse_field_type(self, field_type: str) -> Dict[str, Any]:
        """Parse field type, determining if it's nullable or a list."""
        is_nullable = "!" not in field_type
        is_list = "[" in field_type
        base_type = field_type.replace("!", "").replace("[", "").replace("]", "")
        return {
            "base_type": base_type,
            "is_nullable": is_nullable,
            "is_list": is_list
        }

    def parse(self) -> Dict[str, Dict[str, Any]]:
        """Parse the GraphQL schema from the specified file path."""
        current_type = None

        with open(self.file_path, 'r') as file:
            for line in file:
                line = line.strip()  # Remove leading/trailing whitespace

                # Match the start of a type declaration
                type_match = self.TYPE_REGEX.match(line)
                if type_match:
                    current_type = type_match.group(1)
                    self.schema_dict[current_type] = {}
                    continue

                # Match a field declaration with parameters
                field_match = self.FIELD_WITH_PARAMS_REGEX.match(line)
                if field_match and current_type:
                    field_name = field_match.group(1)
                    parameters = field_match.group(2)
                    return_type = field_match.group(3)

                    self.schema_dict[current_type][field_name] = {
                        "parameters": self.parse_parameters(parameters),
                        "return_type": self.parse_field_type(return_type)
                    }
                    continue

                # Match a simple field without parameters
                simple_field_match = self.SIMPLE_FIELD_REGEX.match(line)
                if simple_field_match and current_type:
                    field_name = simple_field_match.group(1)
                    field_type = simple_field_match.group(2)
                    self.schema_dict[current_type][field_name] = self.parse_field_type(field_type)

        return self.schema_dict