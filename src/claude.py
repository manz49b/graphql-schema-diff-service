import os
from dotenv import load_dotenv
import anthropic

load_dotenv()  # Load environment variables from.env file

def create_message(start_prompt, end_prompt, internal_input, api_key=os.environ.get("CLAUDE_API")):
    """
    Call the Claude API with input inserted in the middle.

    Args:
        start_prompt (str): The starting prompt for the message.
        end_prompt (str): The ending prompt for the message.
        internal_input (str): The internal input for the message.
        api_key (str): The API key for the Claude API.

    Returns:
        str: The generated message from
    """
    client = anthropic.Anthropic(api_key=api_key)
    baseline_tokens = len(start_prompt) + len(end_prompt)

    # Split internal input into chunks to avoid exceeding max tokens
    max_tokens = 1024 - baseline_tokens
    chunks = [internal_input[i:i+max_tokens] for i in range(0, len(internal_input), max_tokens)]

    messages = []
    for chunk in chunks:
        messages.append({"role": "user", "content": chunk})

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": start_prompt},
            *messages,
            {"role": "assistant", "content": end_prompt}
        ]
    )
    return message.content

def create_message(prompt, max_tokens, api_key=os.environ.get("CLAUDE_API")):
    """
    Call the Claude API with a given prompt and return the generated message.

    Args:
        prompt (str): The prompt to send to Claude.
        max_tokens (int): The maximum number of tokens to generate.
        api_key (str): The API key for the Claude API.
    
    Returns:
        str: The generated message from Claude.
    """
    # Check if API key is set
    if not api_key:
        print("Error: CLAUDE_API key is not set in the environment.")
        return None

    # Debugging: Print prompt length and a snippet to ensure it's being passed correctly
    print(f"Debug: Sending prompt to Claude (length: {len(prompt)}): {prompt[:200]}...")  # Only print the first 200 characters for security

    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Debugging: Verify response content
        if not message or not message.content:
            print("Error: Received empty or invalid response from Claude.")
            return None

        print("Debug: Successfully received response from Claude.")
        return message.content

    except Exception as e:
        print(f"Error: Exception occurred while creating message with Claude: {e}")
        return None