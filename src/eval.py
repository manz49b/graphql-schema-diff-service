import json
from nltk.translate.bleu_score import sentence_bleu
from rouge import Rouge

# Function to evaluate BLEU score
def evaluate_bleu(expected, generated):
    return sentence_bleu([expected], generated)

# Function to evaluate ROUGE score
def evaluate_rouge(expected, generated):
    rouge = Rouge()
    scores = rouge.get_scores(generated, expected, avg=True)
    return scores

# Evaluate Accuracy (for exact match)
def evaluate_exact_match(expected, generated):
    return expected == generated

# Perform evaluations
def evaluate_response(expected, generated):
    # Extract summaries for BLEU and ROUGE evaluation
    expected_summary = expected["release_notes"]["summary"]
    generated_summary = generated["release_notes"]["summary"]
    
    # Evaluate metrics
    bleu_score = evaluate_bleu(expected_summary.split(), generated_summary.split())
    rouge_score = evaluate_rouge(expected_summary, generated_summary)
    
    exact_match = evaluate_exact_match(json.dumps(expected), json.dumps(generated))
    
    # Print results
    print(f"BLEU Score: {bleu_score:.4f}")
    print(f"ROUGE Score: {rouge_score}")
    print(f"Exact Match: {exact_match}")