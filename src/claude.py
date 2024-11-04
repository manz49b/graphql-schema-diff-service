import os
from dotenv import load_dotenv
import anthropic

load_dotenv()  # Load environment variables from.env file

def create_message(start_prompt, end_prompt, internal_input, api_key=os.environ.get("CLAUDE_API")):
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
    client = anthropic.Anthropic(api_key=api_key)

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=max_tokens,  # Set max_tokens to your desired value
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content