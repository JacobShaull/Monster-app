from base64 import b64decode
import os

from Fortuna import random_int, random_float
from MonsterLab import Monster
from flask import Flask, render_template, request, current_app
from pandas import DataFrame

from data import Database
from graph import chart
from machine import Machine


SPRINT = 21
APP = Flask(__name__)


@APP.route("/")
def home():
    return render_template(
        "home.html",
        sprint=f"Sprint {SPRINT}",
        monster=Monster().to_dict(),
        password=b64decode(b"VGFuZ2VyaW5lIERyZWFt"),
    )


@APP.route("/data")
def data():
    if SPRINT < 1:
        return render_template("data.html")
    db = Database()
    return render_template(
        "data.html",
        count=db.count(),
        table=db.html_table(),
    )


@APP.route("/view", methods=["GET", "POST"])
def view():
    try:
        if SPRINT < 2:
            return render_template("view.html")
        db = Database()
        options = ["Level", "Health", "Energy", "Sanity", "Rarity"]
        x_axis = request.values.get("x_axis") or options[1]
        y_axis = request.values.get("y_axis") or options[2]
        target = request.values.get("target") or options[4]
        df = db.dataframe()
        current_app.logger.info(f"DataFrame head: {df.head()}")
        graph = chart(
            df=df,
            x=f"{x_axis}:Q",
            y=f"{y_axis}:Q",
            target=f"{target}:N",
        ).to_json()
        return render_template(
            "view.html",
            options=options,
            x_axis=x_axis,
            y_axis=y_axis,
            target=target,
            count=db.count(),
            graph=graph,
        )
    except Exception as e:
        current_app.logger.error(f"An error occurred: {e}")
        raise  # Reraise the exception to get the stack trace in the Flask server output


@APP.route("/model", methods=["GET", "POST"])
def model():
    if SPRINT < 3:
        return render_template("model.html")
    db = Database()
    options = ["Level", "Health", "Energy", "Sanity", "Rarity"]
    filepath = os.path.join("app", "model.joblib")
    if not os.path.exists(filepath):
        df = db.dataframe()
        machine = Machine(df[options])
        machine.save(filepath)
    else:
        machine = Machine.open(filepath)
    stats = [round(random_float(1, 250), 2) for _ in range(3)]
    level = request.values.get("level", type=int) or random_int(1, 20)
    health = request.values.get("health", type=float) or stats.pop()
    energy = request.values.get("energy", type=float) or stats.pop()
    sanity = request.values.get("sanity", type=float) or stats.pop()
    prediction, confidence = machine(DataFrame(
        [dict(zip(options, (level, health, energy, sanity)))]
    ))
    info = machine.info()
    return render_template(
        "model.html",
        info=info,
        level=level,
        health=health,
        energy=energy,
        sanity=sanity,
        prediction=prediction,
        confidence=f"{confidence:.2%}",
    )

@APP.route("/monsters")
def show_monsters():
    db = Database()
    monsters = db.dataframe().to_dict(orient='records')
    print(monsters)  # This will print the data in your Flask console
    return render_template('monsters.html', monsters=monsters)

@APP.route("/seed")
def seed_database():
    db = Database()
    db.seed(1000)  # Adjust the number as needed
    return "Database has been seeded with monsters."



if __name__ == '__main__':
    APP.run(debug=True)
