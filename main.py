import os

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

from tables import Cafe, db

load_dotenv()

app = Flask(__name__)


app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
Bootstrap(app)

# Connect to DB
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/cafes")
def cafes():
    # Grab all cafes
    all_cafes = Cafe.query.all()
    return render_template("cafes.html", cafes=all_cafes)


if __name__ == "__main__":
    app.run(debug=True)
