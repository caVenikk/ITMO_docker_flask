import os
from datetime import datetime
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

db_user = os.getenv("POSTGRES_USER")
db_password = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")
db_host = os.getenv("POSTGRES_HOST")
db_port = os.getenv("POSTGRES_PORT")
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

db = SQLAlchemy(app)


class Counter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, default=datetime.utcnow)
    client_info = db.Column(db.String)


with app.app_context():
    db.create_all()


@app.route("/")
def hello():
    client_info = request.headers.get("User-Agent", "Unknown")
    new_entry = Counter(client_info=client_info)
    db.session.add(new_entry)
    db.session.commit()
    count = Counter.query.count()
    return f"Hello World! I have been seen {count} times.\n"
