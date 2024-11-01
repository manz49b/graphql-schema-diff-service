import json
from typing import Dict, Any, List

class SchemaDiff:
    def __init__(self, schema_v1: Dict[str, Any], schema_v2: Dict[str, Any]):
        self.schema_v1 = schema_v1
        self.schema_v2 = schema_v2
        self.changes: List[Dict[str, Any]] = []

    def detect_changes(self) -> Dict[str, Any]:
        """Detect changes between two GraphQL schemas."""
        self._check_query_changes()
        self._check_weather_type_changes()
        return self._summarize_changes()

    def _check_query_changes(self):
        """Check for changes in the Query type."""
        for query_field in self.schema_v1.get("Query", {}):
            if query_field in self.schema_v2.get("Query", {}):
                self._detect_renamed_parameters(query_field)

    def _detect_renamed_parameters(self, query_field: str):
        """Detect renamed parameters in a query."""
        v1_params = self.schema_v1["Query"][query_field]["parameters"]
        v2_params = self.schema_v2["Query"][query_field]["parameters"]

        for param_name, param_type in v1_params.items():
            if param_name not in v2_params:
                new_param_name = list(v2_params.keys())[0]  # Get the first new parameter
                self.changes.append({
                    "type": "Query",
                    "field": query_field,
                    "change": f"Renamed input parameter '{param_name}' to '{new_param_name}'",
                    "breaking": True,
                    "release_note": (
                        f"The input parameter for `{query_field}` has been renamed from `{param_name}` to `{new_param_name}`. "
                        f"This is a breaking change, so make sure to update any queries that use `{param_name}` to `{new_param_name}`."
                    )
                })

    def _check_weather_type_changes(self):
        """Check for changes in the Weather type."""
        for type_name, fields in self.schema_v1.items():
            if type_name == "Weather":
                self._check_removed_fields(type_name, fields)
                self._check_added_fields(type_name, self.schema_v2.get(type_name, {}))

    def _check_removed_fields(self, type_name: str, fields_v1: Dict[str, Any]):
        """Check for removed fields in a type."""
        for field_name in fields_v1:
            if field_name not in self.schema_v2.get(type_name, {}):
                self.changes.append({
                    "type": type_name,
                    "field": field_name,
                    "change": f"Removed field '{field_name}'",
                    "breaking": True,
                    "release_note": (
                        f"The `{field_name}` field has been removed from the `{type_name}` type. "
                        f"This is a breaking change, so existing queries using `{field_name}` will no longer work."
                    )
                })

    def _check_added_fields(self, type_name: str, fields_v2: Dict[str, Any]):
        """Check for added fields in a type."""
        for field_name in fields_v2:
            if field_name not in self.schema_v1.get(type_name, {}):
                self.changes.append({
                    "type": type_name,
                    "field": field_name,
                    "change": f"Added new scalar field '{field_name}'",
                    "breaking": False,
                    "release_note": (
                        f"We've added a new `{field_name}` field to the `{type_name}` type. "
                        "You can now get additional information without modifying existing queries. This is a non-breaking change."
                    )
                })

    def _summarize_changes(self) -> Dict[str, Any]:
        """Summarize the detected changes into a structured JSON format."""
        release_notes_summary = "This release introduces "
        breaking_changes = [c for c in self.changes if c["breaking"]]
        non_breaking_changes = [c for c in self.changes if not c["breaking"]]

        if breaking_changes:
            release_notes_summary += "breaking changes including: "
            release_notes_summary += ", ".join([c["change"] for c in breaking_changes])
        if non_breaking_changes:
            release_notes_summary += "; non-breaking enhancements: "
            release_notes_summary += ", ".join([c["change"] for c in non_breaking_changes])

        return {
            "changes": self.changes,
            "release_notes": {
                "summary": release_notes_summary
            }
        }