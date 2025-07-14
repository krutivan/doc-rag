
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'rag-app', 'src', 'rag', 'web'))

from asgiref.wsgi import WsgiToAsgi
from app import app

# Convert Flask WSGI app to ASGI
app = WsgiToAsgi(app)
