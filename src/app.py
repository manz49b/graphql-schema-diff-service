from schema_parser import SchemaParser
from schema_diff import SchemaDiff, json
from prompt import get_prompt_7
from claude import create_message
from utils import safe_load_json, save_evaluation_data
from eval import evaluate_response, f1_results, ab_testing, rate_coherence, expert_rubric, identify_edge_cases
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
    python_change_report = schema_diff.detect_changes()

    prompt, prompt_version = get_prompt_7(schema_v1, schema_v2)
    response = create_message(prompt, 4096)
    llm_change_report = safe_load_json(response[0].text)

    metrics = {}
    print("Python Method Scoring:")
    bleu_score, rouge_score, exact_match = evaluate_response(expected_output, python_change_report)
    metrics['llm_bleu_score'] = bleu_score
    metrics['llm_rouge_score'] = rouge_score
    metrics['exact_match'] = exact_match
    f1, precision, recall = f1_results(python_change_report, expected_output)
    metrics['llm_f1'] = f1
    metrics['llm_precision'] = precision
    metrics['llm_recall'] = recall

    print("LLM Scoring:")
    bleu_score, rouge_score, exact_match = evaluate_response(expected_output, llm_change_report)
    metrics['llm_bleu_score'] = bleu_score
    metrics['llm_rouge_score'] = rouge_score
    metrics['exact_match'] = exact_match
    f1, precision, recall = f1_results(llm_change_report, expected_output)
    metrics['llm_f1'] = f1
    metrics['llm_precision'] = precision
    metrics['llm_recall'] = recall

    llm_edge_case_results = identify_edge_cases(llm_change_report, llm_change_report)
    python_edge_case_results = identify_edge_cases(python_change_report, python_change_report)

    metrics['llm_edge_cases'] = llm_edge_case_results
    metrics['python_edge_cases'] = python_edge_case_results

    llm_pref, python_pref = ab_testing(llm_change_report, python_change_report)
    metrics['llm_pref'] = llm_pref
    metrics['python_pref'] = python_pref

    llm_coherence_score, llm_ratings = rate_coherence(llm_change_report)
    python_coherence_score, python_ratings = rate_coherence(python_change_report)

    metrics['llm_coherence_score'] = llm_coherence_score
    metrics['python_coherence_score'] = python_coherence_score
    metrics['llm_ratings'] = llm_ratings
    metrics['python_ratings'] = python_ratings

    llm_rubric_score, llm_rubric_details = expert_rubric(llm_change_report)
    python_rubric_score, python_rubric_details = expert_rubric(python_change_report)

    metrics['llm_rubric_score'] = llm_rubric_score
    metrics['python_rubric_score'] = python_rubric_score
    metrics['llm_rubric_details'] = llm_rubric_details
    metrics['python_rubric_details'] = python_rubric_details

    save_evaluation_data(example, prompt, prompt_version, llm_change_report, python_change_report, expected_output, metrics)

if __name__ == "__main__":
    main()
