from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

from app import create_app, db

# --- ¡ESTA ES LA LÍNEA QUE ARREGLA TODO! ---
# La sacamos del 'if' para que Render la pueda ver
app = create_app()
# -------------------------------------------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)