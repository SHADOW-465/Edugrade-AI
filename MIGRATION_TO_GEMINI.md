# Migration Guide: OpenAI to Google Gemini

This guide helps you migrate from OpenAI API to Google Gemini API in EduGrade AI.

## What Changed

- **AI Model**: Switched from GPT-4o-mini to Google Gemini 1.5 Flash
- **API Key**: Changed from `OPENAI_API_KEY` to `GOOGLE_GEMINI_API_KEY`
- **Dependencies**: Replaced `openai` package with `google-generativeai`

## Migration Steps

### 1. Update Environment Variables

**Before:**
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

**After:**
```bash
GOOGLE_GEMINI_API_KEY=your_google_gemini_api_key_here
```

### 2. Get Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

### 3. Update Your .env File

```bash
# Remove or comment out the old OpenAI key
# OPENAI_API_KEY=your_old_key

# Add your new Gemini key
GOOGLE_GEMINI_API_KEY=your_new_gemini_key
```

### 4. Reinstall Dependencies

```bash
pip uninstall openai
pip install google-generativeai
```

Or simply reinstall all requirements:
```bash
pip install -r requirements.txt
```

### 5. Test the Setup

Run the setup script to test your configuration:
```bash
python scripts/setup_gemini.py
```

## Benefits of Google Gemini

- **Cost Effective**: Generally more cost-effective than OpenAI
- **Fast Response**: Quick response times for evaluation tasks
- **Multimodal**: Better support for image and text processing
- **JSON Output**: Native support for structured JSON responses

## API Usage Comparison

### OpenAI (Old)
```python
response = await openai.ChatCompletion.acreate(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.3
)
```

### Google Gemini (New)
```python
response = await asyncio.get_event_loop().run_in_executor(
    None,
    lambda: model.generate_content(prompt, generation_config=config)
)
```

## Troubleshooting

### Common Issues

1. **Import Error**: Make sure you have `google-generativeai` installed
2. **API Key Error**: Verify your Gemini API key is correct
3. **Rate Limits**: Gemini has different rate limits than OpenAI

### Getting Help

- Check the [Google AI documentation](https://ai.google.dev/docs)
- Review the EduGrade AI logs for specific error messages
- Ensure your API key has the necessary permissions

## Performance Notes

- Gemini 1.5 Flash is optimized for speed and efficiency
- Response times may vary compared to OpenAI
- JSON output is more reliable with Gemini's structured generation

## Rollback (if needed)

If you need to rollback to OpenAI:

1. Revert the code changes
2. Install OpenAI: `pip install openai`
3. Set `OPENAI_API_KEY` in your environment
4. Restart the application

---

**Note**: This migration maintains full compatibility with existing grade data and configurations.
