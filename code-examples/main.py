#!/usr/bin/env python3
from flask import Flask, render_template, request, redirect, url_for

app = Flask("Mitt Zoo")


animals = [
    {"type": "Zebra", "name": "Stripes", "legs": 4},
    {"type": "Lejon", "name": "Simba", "legs": 4, "image": "lejon.jpeg"},
    {"type": "Fisk", "name": "Nemo", "legs" : 0},
    {"type": "Struts", "name": "Hals", "legs" : 2, "image": "struts.jpeg"},
]

@app.route("/")
def index():
    global animals
    username = request.args.get("username", "Anonym")
    return render_template("index.html", name=username, animals=animals)

@app.route("/info/<int:id>")
def info(id):
    global animals
    return render_template("info.html", animal=animals[id], legs="."*animals[id]["legs"], id=id)

@app.route("/add", methods=["GET", "POST"])
def add():
    global animals
    if "name" in request.form:
        animals.append(
            {"type": "?", "name": request.form["name"], "legs": 4},
        )
        return redirect(url_for("index"))
    return render_template("add.html")

@app.route("/remove", methods=["POST"])
def remove():
    global animals
    if "id" in request.form:
        del animals[int(request.form["id"])]
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
