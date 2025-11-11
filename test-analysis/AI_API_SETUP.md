# AI API Setup for Test Alignment

The `_align_test_implementations` method now supports AI API integration to generate code modifications automatically.

## Supported AI Providers

1. **OpenAI** (GPT-4)
2. **Anthropic** (Claude)
3. **Cursor AI** (Fallback - uses built-in capabilities)

## Setup Instructions

### Option 1: OpenAI API

1. Get your API key from https://platform.openai.com/api-keys
2. Set environment variable:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
3. (Optional) Set model:
   ```bash
   export OPENAI_MODEL="gpt-4-turbo-preview"  # Default
   ```
4. Install library:
   ```bash
   pip install openai
   ```

### Option 2: Anthropic API

1. Get your API key from https://console.anthropic.com/
2. Set environment variable:
   ```bash
   export ANTHROPIC_API_KEY="your-api-key-here"
   ```
3. (Optional) Set model:
   ```bash
   export ANTHROPIC_MODEL="claude-3-5-sonnet-20241022"  # Default
   ```
4. Install library:
   ```bash
   pip install anthropic
   ```

### Option 3: Cursor AI (No Setup Required)

If no API keys are configured, the system will:
- Provide diagnostic information
- Suggest manual review using Cursor's built-in AI
- You can then use Cursor's AI features to fix the tests interactively

## How It Works

When `_align_test_implementations` is called:

1. First tries pattern-based fixes (missing assertions, etc.)
2. If no pattern fixes found, calls AI API with:
   - TypeScript test code (reference)
   - Python test code (current)
   - Context (similarity scores, differences, etc.)
3. AI returns a `TestModification` with:
   - `old_code`: Exact code to replace
   - `new_code`: Modified code aligned with TypeScript
   - `explanation`: What was changed and why
   - `confidence`: Confidence score (0.0-1.0)

## Example Usage

```bash
# Set API key
export OPENAI_API_KEY="sk-..."

# Run test fixer
python3 auto_test_fixer.py --max-tests 1
```

The AI will automatically be called when alignment is needed.

## Cost Considerations

- OpenAI GPT-4: ~$0.01-0.03 per test alignment
- Anthropic Claude: ~$0.015-0.03 per test alignment
- Costs depend on code length and complexity

## Troubleshooting

### "OpenAI library not installed"
```bash
pip install openai
```

### "Anthropic library not installed"
```bash
pip install anthropic
```

### "No AI API key configured"
Set one of the environment variables above, or use Cursor's built-in AI for manual fixes.

### API Errors
- Check your API key is valid
- Check you have sufficient credits/quota
- Check network connectivity
- Review error messages in the output



