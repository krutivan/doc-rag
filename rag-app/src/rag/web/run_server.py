import uvicorn

from asgiref.wsgi import WsgiToAsgi

from app import app

# Convert Flask WSGI app to ASGI
asgi_app = WsgiToAsgi(app)

def run_flask_server():
  """Run Flask app with uvicorn ASGI server"""
  uvicorn.run("run_server:asgi_app",
              host="0.0.0.0",
              port=5000,
              reload=True,
              log_level="info")


if __name__ == "__main__":
  run_flask_server()
