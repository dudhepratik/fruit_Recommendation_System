from flask import Blueprint, request, redirect, url_for
from models.feedback import save_feedback, load_feedback_data, train_model

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/feedback', methods=['POST'])
def feedback():
    user_input = request.form['user_input']
    recommendation = request.form['recommendation']
    feedback = request.form['feedback']
    additional_feedback = request.form.get('additional_feedback', '')

    save_feedback(user_input, recommendation, feedback, additional_feedback)

    feedback_data = load_feedback_data()
    train_model(feedback_data)

    return redirect(url_for('recommend.index'))
