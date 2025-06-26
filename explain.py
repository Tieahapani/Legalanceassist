import anthropic
from config import ANTHROPIC_API_KEY
from deep_translator import GoogleTranslator

# ✅ Initialize the client
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def simplify_with_claude(text, target_language="english"):
    prompt = f"""
You are Legalance, a friendly assistant for explaining immigration rights in plain English.

Please rewrite the following legal explanation in a way that's simple, supportive, and easy to understand. Avoid legal jargon and keep it under 100 words.

---START---
{text}
---END---
"""

    # ✅ Correct indentation
    response = client.beta.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt}
                ]
            }
        ]
    )

    simplified_english = response.content[0].text.strip()

    # ✅ Translate if needed
    if target_language.lower() != "english":
        return GoogleTranslator(source='auto', target=target_language).translate(simplified_english)

    return simplified_english
