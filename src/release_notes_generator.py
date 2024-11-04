from transformers import T5Tokenizer, T5ForConditionalGeneration

class ReleaseNotesGenerator:
    def __init__(self):
        self.tokenizer = T5Tokenizer.from_pretrained('t5-small')
        self.model = T5ForConditionalGeneration.from_pretrained('t5-small')
    
    def generate_notes(self, changes: Dict[str, List[str]]) -> str:
        """Generate release notes from breaking changes."""
        input_text = "Generate release notes based on the following changes: "
        for change, items in changes.items():
            input_text += f"{change}: {', '.join(items)}; "
        
        inputs = self.tokenizer.encode("summarize: " + input_text, return_tensors='pt')
        outputs = self.model.generate(inputs, max_length=500)
        notes = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return notes

# Example usage
generator = ReleaseNotesGenerator()
changes = compare_schemas(ast1, ast2)
notes = generator.generate_notes(changes)
print(notes)