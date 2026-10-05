import ollama
import json

def extract_structured_data(entry_text):
    """Send entry to Ollama to extract structured JSON data."""
    prompt = f"""
    Analyze this journal entry and extract information into JSON format.
    Use exactly these keys:
    - event: A 3-6 word summary of what happened.
    - situation: A one-sentence description of the situation.
    - emotions: A list of emotions chosen ONLY from this list: ["calm", "anxious", "sad", "angry", "happy", "frustrated", "numb", "excited", "overwhelmed", "disappointed"].
    - intensity: Choose from ["low", "medium", "high"].
    - triggers: A list of specific causes (e.g., ["failed test", "comparison with friends"]).

    Entry: "{entry_text}"
    """
    try:
        # Call the local model. Format="json" forces valid JSON output.
        response = ollama.generate(
            model='deepseek-r1:1.5b',
            prompt=prompt,
            format='json'
        )
        return json.loads(response['response'])
    except Exception as e:
        print(f"Error extracting data: {e}")
        # Fallback if Ollama fails or parsing fails
        return {
            "event": "Analysis failed",
            "situation": "Could not parse entry.",
            "emotions": ["numb"],
            "intensity": "low",
            "triggers": []
        }
def extract_preferences(entry_text):
    """Extract explicit preferences the user states."""
    prompt = f"""
    Extract ONLY explicit preferences the user states (e.g., favorite person, food, places like where they study, activities, subjects).
    Do not infer unstated preferences. Return an empty list if none are found.
    Format as JSON list of objects with keys: "category", "value", "evidence".
    Entry: "{entry_text}"
    """
    try:
        response = ollama.generate(model='deepseek-r1:1.5b', prompt=prompt, format='json')
        result = json.loads(response['response'])
        return result if isinstance(result, list) else []
    except Exception as e:
        return []

def extract_entities(entry_text):
    """Extract named entities from the journal entry."""
    prompt = f"""
    Extract named entities from this journal entry: exams, people, subjects, places, recurring events (e.g. ["CAT 2", "maths", "library", "Priya"]).
    Return ONLY a JSON list of strings. Empty list allowed.
    Entry: "{entry_text}"
    """
    try:
        response = ollama.generate(model='deepseek-r1:1.5b', prompt=prompt, format='json')
        result = json.loads(response['response'])
        return result if isinstance(result, list) else []
    except Exception as e:
        return []
