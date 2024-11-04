import json

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