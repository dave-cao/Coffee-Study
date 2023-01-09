import os

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, url_for
from flask_bootstrap import Bootstrap

from forms import CafeForm
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
    all_cafes = Cafe.query.all()[::-1]
    return render_template("cafes.html", cafes=all_cafes)


@app.route("/add", methods=["GET", "POST"])
def add():
    form = CafeForm()
    if form.validate_on_submit():
        coffee_price = "$" + "%.2f" % form.coffee_price.data
        new_cafe = Cafe(
            name=form.cafe_name.data,
            map_url=form.map_url.data,
            img_url=form.img_url.data,
            location=form.location.data,
            seats=form.seats.data,
            has_toilet=form.has_toilet.data,
            has_wifi=form.has_wifi.data,
            has_sockets=form.has_sockets.data,
            can_take_calls=form.can_take_calls.data,
            coffee_price=coffee_price,
        )

        # add to database
        db.session.add(new_cafe)
        db.session.commit()

        return redirect(url_for("cafes"))

    return render_template("add.html", form=form)


@app.route("/edit<int:cafe_id>", methods=["GET", "POST"])
def edit(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    form = CafeForm(
        cafe_name=cafe.name,
        map_url=cafe.map_url,
        img_url=cafe.img_url,
        location=cafe.location,
        seats=cafe.seats,
        coffee_price=cafe.coffee_price[1:],
        has_toilet=cafe.has_toilet,
        has_wifi=cafe.has_wifi,
        has_sockets=cafe.has_sockets,
        can_take_calls=cafe.can_take_calls,
    )
    if form.validate_on_submit():
        coffee_price = "$" + "%.2f" % form.coffee_price.data
        cafe.name = form.cafe_name.data
        cafe.map_url = form.map_url.data
        cafe.img_url = form.img_url.data
        cafe.location = form.location.data
        cafe.seats = form.seats.data
        cafe.has_toilet = form.has_toilet.data
        cafe.has_wifi = form.has_wifi.data
        cafe.has_sockets = form.has_sockets.data
        cafe.can_take_calls = form.can_take_calls.data
        cafe.coffee_price = coffee_price
        db.session.commit()

        return redirect(url_for("cafes"))

    return render_template("add.html", form=form)


@app.route("/delete<int:cafe_id>")
def delete(cafe_id):
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for("cafes"))


if __name__ == "__main__":
    app.run(debug=True)
