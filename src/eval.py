import json
from sklearn.metrics import precision_score, recall_score, f1_score
from nltk.translate.bleu_score import sentence_bleu
from nltk.tokenize import word_tokenize
from rouge import Rouge
import random
import numpy as np
import nltk

# Download punkt tokenizer and its components
nltk.download('punkt', download_dir='/opt/homebrew/Caskroom/mambaforge/base/envs/graphql-schema-diff-service/lib/nltk_data')
nltk.download('punkt_tab', download_dir='/opt/homebrew/Caskroom/mambaforge/base/envs/graphql-schema-diff-service/lib/nltk_data')

def tokenize_output(output):
    """ Tokenizes the changes and release notes for BLEU score calculation. """
    # Join all changes and release notes into a single string
    generated_text = ' '.join([
        change['release_note'] for change in output['changes']
    ]) + ' ' + output['release_notes']['summary']

    # Tokenize the text
    return word_tokenize(generated_text.lower())

def evaluate_bleu(expected, generated):
    """ Evaluates BLEU score between expected and generated outputs. """
    # Tokenize expected output
    expected_text = ' '.join([
        change['release_note'] for change in expected['changes']
    ]) + ' ' + expected['release_notes']['summary']
    
    # Tokenize both expected and generated texts
    expected_tokens = tokenize_output(expected)
    generated_tokens = tokenize_output(generated)

    # Calculate BLEU score
    score = sentence_bleu([expected_tokens], generated_tokens)
    return score

def tokenize_text(output):
    """ Tokenizes the changes and release notes for ROUGE score calculation. """
    
    if not isinstance(output, dict):
        raise ValueError("Expected a dictionary for output.")

    if 'changes' not in output or 'release_notes' not in output:
        raise KeyError("Expected keys 'changes' and 'release_notes' in output.")
    
    # Join all changes and release notes into a single string
    text = ' '.join([
        change['release_note'] for change in output['changes']
    ]) + ' ' + output['release_notes']['summary']
    
    return text

def evaluate_rouge(expected, generated):
    """ Evaluates ROUGE score between expected and generated output. """
    
    expected_text = tokenize_text(expected)
    generated_text = tokenize_text(generated)
    
    # Initialize ROUGE
    rouge = Rouge()
    
    # Calculate ROUGE scores
    scores = rouge.get_scores(generated_text, expected_text, avg=True)
    return scores

def evaluate_exact_match(expected, generated):
    return expected == generated

def evaluate_response(expected, generated):
    # Evaluate metrics
    bleu_score = evaluate_bleu(expected, generated)
    rouge_score = evaluate_rouge(expected, generated)
    exact_match = evaluate_exact_match(json.dumps(expected), json.dumps(generated))
    
    # Print results
    print(f"BLEU Score: {bleu_score:.4f}")
    print(f"ROUGE Score: {rouge_score}")
    print(f"Exact Match: {exact_match}")

# Function to evaluate field-level precision, recall, and F1
def evaluate_field_level(response, ideal, key):
    # Lists to store binary indicators of matches
    y_true = []
    y_pred = []
    
    # Compare each entry in `changes` list at the field level
    for entry_res, entry_ideal in zip(response[key], ideal[key]):
        for field in entry_ideal.keys():
            # 1 if the field matches the ideal, 0 if it doesn't
            y_true.append(1)  # Ideal output should have all correct fields
            y_pred.append(1 if entry_res[field] == entry_ideal[field] else 0)
    
    # Use sklearn metrics to calculate precision, recall, and F1 score
    precision = precision_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)

    return precision, recall, f1

def f1_results(test_output, expected_output):
    precision, recall, f1 = evaluate_field_level(test_output, expected_output, "changes")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1 Score: {f1:.4f}")

# Simulate A/B testing
def ab_testing(llm_response, expected_output):
    # Simulated user feedback: randomly choose a preferred response
    preferences = {"llm": 0, "python": 0}
    
    for _ in range(100):  # Simulate 100 users
        preferred = random.choice(["llm", "python"])
        preferences[preferred] += 1
    
    # Calculate A/B test results
    total = sum(preferences.values())
    llm_preference_percentage = (preferences["llm"] / total) * 100
    python_preference_percentage = (preferences["python"] / total) * 100
    
    return llm_preference_percentage, python_preference_percentage

# Function to simulate or input Likert scale scores
def rate_coherence(response):
    # Human raters assign scores between 1 to 5 for coherence
    # Example rating structure
    ratings = {
        "clarity": 4,   # How clear is the output? (1-5)
        "consistency": 5,  # Is the output internally consistent? (1-5)
        "fluency": 4,   # Is the text fluent and well-written? (1-5)
        "relevance": 4  # Is the content relevant to the task? (1-5)
    }
    
    # Calculate average score across criteria
    average_score = np.mean(list(ratings.values()))
    return average_score, ratings

# Function for expert rubric ratings
def expert_rubric(response):
    # Raters assign scores on each criterion (1-5 scale, for example)
    rubric = {
        "accuracy": 4,   # How accurate is the information? (1-5)
        "appropriateness": 5,  # Is the tone/style appropriate for the task? (1-5)
        "grammar": 4,    # How grammatically correct is the text? (1-5)
        "domain_relevance": 5  # Is it relevant to the domain/topic? (1-5)
    }
    
    # Average score across rubric criteria
    average_score = np.mean(list(rubric.values()))
    return average_score, rubric

def identify_edge_cases(reference, test_report):
    edge_cases = []

    # Check for edge case 1: Renamed fields with special characters or casing
    for change in reference["changes"]:
        if "field" in change and (any(char in change["field"] for char in ['$', '%', '@'])):
            edge_cases.append({"edge_case": "Special characters in field names", "matched": change["field"] in test_report["changes"]})

    # Check for edge case 2: New fields with unusual data types
    # This is an example; you'd implement actual checks based on your schema rules
    for change in test_report["changes"]:
        if change["type"] == "Weather" and "visibility" in change["field"] and "Int" not in change["change"]:
            edge_cases.append({"edge_case": "Unexpected data type for 'visibility'", "matched": False})

    # Add more edge case checks as needed
    # Edge case 3: No changes
    if len(reference["changes"]) == 0 and len(test_report["changes"]) == 0:
        edge_cases.append({"edge_case": "No changes present", "matched": True})

    return edge_cases
