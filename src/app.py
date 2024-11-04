from schema_parser import SchemaParser
from schema_diff import SchemaDiff, json
from prompt import get_prompt
from claude import create_message
from json_tools import safe_load_json
from eval import evaluate_response
from base import DATA_PATH

def main():
    examples = ["example","example-1"]
    # Just test one example for now
    example = examples[0]

    schema_v1_parser = SchemaParser(f'{DATA_PATH}/schema-1-{example}.txt')
    schema_v1 = schema_v1_parser.parse()

    schema_v2_parser = SchemaParser(f'{DATA_PATH}/schema-2-{example}.txt')
    schema_v2 = schema_v2_parser.parse()

    output_path = (f'{DATA_PATH}/output-{example}.txt')
    with open(output_path, 'r') as file:
        expected_output = json.load(file)
        
    schema_diff = SchemaDiff(schema_v1, schema_v2)
    change_report = schema_diff.detect_changes()
    # Python change report
    print(json.dumps(change_report, indent=2))

    prompt = get_prompt(schema_v1, schema_v2)
    response = create_message(prompt, 2048)
    # LLM change report
    llm_change_report = safe_load_json(response[0].text)
    print(response)

    evaluate_response(expected_output, llm_change_report)
    evaluate_response(expected_output, change_report)


if __name__ == "__main__":
    main()
