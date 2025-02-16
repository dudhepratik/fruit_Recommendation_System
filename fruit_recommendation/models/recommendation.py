import spacy
from fuzzywuzzy import process
from db import get_db_connection

nlp = spacy.load("en_core_web_sm")

def process_input(user_input):
    """Preprocess user input using NLP."""
    doc = nlp(user_input)
    return [token.text.lower() for token in doc if token.is_alpha]

def fuzzy_match(column_list, keyword):
    """Fuzzy match for disease, condition, and symptoms."""
    matches = process.extract(keyword, column_list, limit=3)
    for match, score in matches:
        if score > 70:
            return match
    return None

def recommend_fruits(keywords):
    """Fetch recommendation from database."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM fruits")
    fruits_data = cursor.fetchall()
    conn.close()

    disease_list = [f['Disease Name'] for f in fruits_data]
    conditions_list = [f['Associated Conditions'] for f in fruits_data]
    symptoms_list = [f['Symptoms'] for f in fruits_data]

    matched_rows = []
    for keyword in keywords:
        disease_match = fuzzy_match(disease_list, keyword)
        condition_match = fuzzy_match(conditions_list, keyword)
        symptom_match = fuzzy_match(symptoms_list, keyword)

        if disease_match:
            matched_rows.extend([f for f in fruits_data if disease_match in f['Disease Name']])
        if condition_match:
            matched_rows.extend([f for f in fruits_data if condition_match in f['Associated Conditions']])
        if symptom_match:
            matched_rows.extend([f for f in fruits_data if symptom_match in f['Symptoms']])

    if matched_rows:
        best_match = max(matched_rows, key=lambda row: sum(keyword in str(row.values()).lower() for keyword in keywords))
        def safe_get(key, default="N/A"):
            return best_match.get(key, default)
        
        return {
            "Fruits": f"{safe_get('Fruit 1')}, {safe_get('Fruit 2')}",
            "Recommended Nutrients": safe_get('Recommended Nutrients'),
            "Calories": safe_get('Calories/100g'),
            "Vitamins": safe_get('Vitamins'),
            "Minerals": safe_get('Minerals'),
            "Fiber Content": safe_get('Fiber Cont/100g'),
            "Sugar Content": safe_get('Sugar Content/100g'),
            "Glycemic Index": safe_get('Glycemic Index/100g'),
            "Dietary Restrictions": safe_get('Dietary Restrictions'),
            "District/State": safe_get('District/State'),
            "Seasonality": f"{safe_get('Season 1')} / {safe_get('Season 2')}",
            "Alternative Fruit": safe_get('Alternative Fruit (Off-Season)'),
            "Associated Conditions": safe_get('Associated Conditions'),
            "Symptoms": safe_get('Symptoms')
        }
    return None
