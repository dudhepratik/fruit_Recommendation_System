from flask import Flask
from routes.recommend import recommend_bp
from routes.feedback import feedback_bp

app = Flask(__name__)

# Register Blueprints
app.register_blueprint(recommend_bp)
app.register_blueprint(feedback_bp)

if __name__ == "__main__":
    app.run(debug=True)
