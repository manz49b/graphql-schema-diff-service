import unittest
import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.eval import (
    tokenize_output,
    evaluate_bleu,
    evaluate_rouge,
    evaluate_exact_match,
    evaluate_field_level,
    f1_results,
    ab_testing,
    rate_coherence,
    expert_rubric,
    identify_edge_cases
)

class TestEvaluationMetrics(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Load expected output from the JSON file
        with open('/Users/bevmanz/Documents/local_code/graphql-schema-diff-service/data/output-example.txt') as f:
            cls.expected_output = json.load(f)

        # Set up common generated output for tests
        cls.generated_output = {
            "changes": [
                {"type": "Query", "field": "getWeather", "change": "Renamed input parameter 'location' to 'city'", "breaking": True, 
                 "release_note": "The input parameter for `getWeather` has been renamed from `location` to `city`. This is a breaking change."},
                {"type": "Weather", "field": "visibility", "change": "Added new Int field 'visibility'", "breaking": False, 
                 "release_note": "We've added a new `visibility` field to the `Weather` type."}
            ],
            "release_notes": {
                "summary": "This release introduces a breaking change with the renaming of the `location` parameter to `city`."
            }
        }

        cls.different_output = {
            "changes": [
                {"type": "Weather", "field": "pressure", "change": "Added new Int field 'pressure'", "breaking": False, 
                 "release_note": "We've added a new `pressure` field to the `Weather` type."}
            ],
            "release_notes": {
                "summary": "This release introduces a new `pressure` field."
            }
        }

    def test_evaluate_bleu_identical(self):
        """Test BLEU score when expected and generated outputs are identical."""
        # Assuming self.expected_output and self.generated_output are set up correctly
        self.generated_output = self.expected_output  # Ensure both are identical
        score = evaluate_bleu(self.expected_output, self.generated_output)
        self.assertAlmostEqual(score, 1.0, places=4, msg="BLEU score should be 1.0 for identical outputs.")

    def test_evaluate_bleu_different(self):
        """Test BLEU score with different expected and generated outputs."""
        # Create a different output that is clearly different from the expected output
        self.different_output = {
            'changes': [{'release_note': 'Some different change note'}],
            'release_notes': {'summary': 'This is a different summary.'}
        }
        
        score = evaluate_bleu(self.expected_output, self.different_output)
        self.assertLess(score, 1.0, msg="BLEU score should be less than 1.0 for different outputs.")

    def test_evaluate_rouge_identical(self):
        """Test ROUGE score when expected and generated outputs are identical."""
        scores = evaluate_rouge(self.expected_output, self.generated_output)
        self.assertAlmostEqual(scores['rouge-1']['f'], 1.0, places=4, msg="ROUGE-1 F score should be 1.0 for identical outputs.")
        self.assertAlmostEqual(scores['rouge-l']['f'], 1.0, places=4, msg="ROUGE-L F score should be 1.0 for identical outputs.")

    def test_evaluate_rouge_different(self):
        """Test ROUGE score with different expected and generated outputs."""
        scores = evaluate_rouge(self.expected_output, self.different_output)
        self.assertLess(scores['rouge-1']['f'], 1.0, msg="ROUGE-1 F score should be less than 1.0 for different outputs.")
        self.assertLess(scores['rouge-l']['f'], 1.0, msg="ROUGE-L F score should be less than 1.0 for different outputs.")
        
    def test_evaluate_exact_match_identical(self):
        """Test exact match when expected and generated outputs are identical."""
        match = evaluate_exact_match(self.expected_output, self.generated_output)
        self.assertTrue(match, "Exact match should return True for identical outputs.")

    def test_evaluate_exact_match_different(self):
        """Test exact match when expected and generated outputs are different."""
        match = evaluate_exact_match(self.expected_output, self.different_output)
        self.assertFalse(match, "Exact match should return False for different outputs.")

    def test_tokenize_output(self):
        """Test the output of the tokenizer."""
        tokenized_text = {
            "changes": [
                {"release_note": "This is a test sentence."}
            ],
            "release_notes": {"summary": ""}
        }
        expected_tokenized = ["this", "is", "a", "test", "sentence", "."]
        tokenized = tokenize_output(tokenized_text)
        self.assertEqual(tokenized, expected_tokenized, "Tokenized output does not match expected output.")

    def test_f1_results(self):
        """Test F1 score calculation."""
        f1, precision, recall = f1_results(self.generated_output, self.expected_output)
        self.assertAlmostEqual(f1, 0.6667, places=4, msg="F1 score calculation is incorrect.")

    def test_ab_testing(self):
        """Test A/B testing evaluation."""
        result_a = {"metric": 0.8}  # Sample LLM response
        result_b = {"metric": 0.6}  # Sample expected output
        
        result = ab_testing(result_a, result_b)
        
        # Check if the result is a tuple
        self.assertIsInstance(result, tuple, "A/B testing should return a tuple.")
        
        # Optionally, check that the tuple has exactly two elements
        self.assertEqual(len(result), 2, "A/B testing should return a tuple with two values.")
        
        # Optionally, you can check that the values are within a reasonable range (0 to 100)
        self.assertTrue(0 <= result[0] <= 100, "LLM preference percentage should be between 0 and 100.")
        self.assertTrue(0 <= result[1] <= 100, "Python preference percentage should be between 0 and 100.")

    def test_expert_rubric(self):
        """Test expert rubric evaluation."""
        rubric_score = expert_rubric(self.expected_output)
        self.assertIsInstance(rubric_score[0], float, "Expert rubric score should be a float.")  # Check the average score
        self.assertIsInstance(rubric_score[1], dict, "Expert rubric breakdown should return a dictionary.")  # Check the breakdown
    
    def test_evaluate_field_level(self):
        """Test field-level evaluation metrics."""
        results = evaluate_field_level(self.generated_output, self.expected_output, "changes")  # Include 'key'
        self.assertIsInstance(results, tuple, "Field level evaluation should return a tuple.")

    def test_identify_edge_cases(self):
        """Test edge case identification."""
        edge_cases = identify_edge_cases(self.expected_output, self.generated_output)  # Provide test_report
        self.assertIsInstance(edge_cases, list, "Edge case identification should return a list.")

    def test_rate_coherence(self):
        """Test coherence rating."""
        average_score, _ = rate_coherence(self.generated_output)  # Call with one argument
        self.assertIsInstance(average_score, float, "Coherence rating should return a float.")


if __name__ == "__main__":
    unittest.main()
