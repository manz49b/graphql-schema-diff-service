from schema_parser import SchemaParser
from schema_diff import SchemaDiff, json
from base import DATA_PATH

def main():
    # Load schemas from .txt files
    schema_v1_parser = SchemaParser(f'{DATA_PATH}/schema-1-example.txt')
    schema_v1 = schema_v1_parser.parse()

    schema_v2_parser = SchemaParser(f'{DATA_PATH}/schema-2-example.txt')
    schema_v2 = schema_v2_parser.parse()

    schema_diff = SchemaDiff(schema_v1, schema_v2)
    change_report = schema_diff.detect_changes()
    print(json.dumps(change_report, indent=2))


if __name__ == "__main__":
    main()
