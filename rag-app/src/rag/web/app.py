
from flask import Flask
from routers.health import health_bp
from routers.chat import chat_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(health_bp)
app.register_blueprint(chat_bp)

@app.route('/')
def home():
    return {"message": "RAG App is running", "status": "ok"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
