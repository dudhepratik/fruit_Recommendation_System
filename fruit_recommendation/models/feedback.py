import numpy as np
from db import get_db_connection
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

def save_feedback(user_input, recommendation, feedback, additional_feedback):
    """Save feedback in MySQL database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO feedback (user_input, recommendation, feedback, additional_feedback) VALUES (%s, %s, %s, %s)",
        (user_input, recommendation, feedback, additional_feedback)
    )
    conn.commit()
    conn.close()

def load_feedback_data():
    """Fetch feedback data for model training."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM feedback")
    feedback_data = cursor.fetchall()
    conn.close()
    return feedback_data


def train_model(feedback_data):
    """Train Logistic Regression model with feedback data."""
    if len(feedback_data) < 2:
        print("Not enough data to train the model. Please collect more feedback.")
        return

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform([f['user_input'] for f in feedback_data])
    y = [1 if f['feedback'].lower() == 'yes' else 0 for f in feedback_data]

    # Check if we have both classes
    if len(set(y)) < 2:
        print("Training failed: Only one class found in data. Collect more diverse feedback.")
        return

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression()
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    print(f"Model accuracy: {accuracy:.2f}")

