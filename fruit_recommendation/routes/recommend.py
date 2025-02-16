from flask import Blueprint, request, render_template
from models.recommendation import process_input, recommend_fruits

recommend_bp = Blueprint('recommend', __name__)

@recommend_bp.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@recommend_bp.route('/recommend', methods=['POST'])
def recommend():
    user_input = request.form['user_input']
    keywords = process_input(user_input)
    recommendation = recommend_fruits(keywords)
    return render_template('index.html', recommendation=recommendation if recommendation else "No match found.")
