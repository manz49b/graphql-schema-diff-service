import json
import os
import pandas as pd
from base import DATA_PATH

def safe_load_json(response_text, default_value=None):
    """
    Safely loads JSON data from a response text.

    Args:
        response_text (str): The JSON string to be loaded.
        default_value (any): Value to return in case of an error (default: None).

    Returns:
        dict: The loaded JSON data if successful, otherwise default_value.
    """
    try:
        # Attempt to load the JSON data
        json_data = json.loads(response_text)
        return json_data
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")  # Log the error
        return default_value
    except Exception as e:
        print(f"An error occurred while loading JSON: {e}")  # Log unexpected errors
        return default_value

def save_evaluation_data(example, prompt, prompt_version, llm_change_report, python_change_report, expected_output, metrics):
    """ Save evaluation data to a Parquet file. """
    output_directory = f"{DATA_PATH}/evaluations/"
    os.makedirs(output_directory, exist_ok=True)  # Create the directory if it doesn't exist
    
    # Prepare data to save in a DataFrame
    evaluation_data = {
        'example_no': example,
        'prompt': prompt,
        'llm_change_report': [json.dumps(llm_change_report)],  # Store as JSON string for Parquet
        'python_change_report': [json.dumps(python_change_report)],  # Store as JSON string for Parquet
        'expected_output': [json.dumps(expected_output)],  # Store as JSON string for Parquet
        **{k: [v] for k, v in metrics.items()}  # Flatten metrics into a dict of lists
    }
    
    # Create a DataFrame
    df = pd.DataFrame(evaluation_data)
    
    # Write data to Parquet file
    output_file_path = os.path.join(output_directory, f'evaluation-{example}_prompt-{prompt_version}.parquet')
    df.to_parquet(output_file_path, index=False)