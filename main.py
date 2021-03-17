from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_restful import Api, Resource
from api import api_blueprint
from database import *
from datetime import date


app = Flask(__name__)
app.secret_key = "secrethelloworldkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db.init_app(app)
with app.app_context():
    db.create_all()
app.register_blueprint(api_blueprint, url_prefix="/words/")


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("index.html")


@app.route('/signup/', methods=["GET", "POST"])
def signup():
    if "user" in session:
        return redirect(url_for("profile"))
    if request.method == "POST":
        user_exists = User.query.filter_by(username=request.form["login"]).first()
        email_occupied = User.query.filter_by(email=request.form["email"]).first()
        passwords_match = request.form["password"] == request.form["repeated_password"]
        if not user_exists and not email_occupied and passwords_match:
            new_user = User(username=request.form["login"],
                            email=request.form["email"],
                            password=request.form["password"])
            db.session.add(new_user)
            db.session.commit()
            session["user"] = new_user.username
            return redirect(url_for("profile"))
        if user_exists:
            flash("The name you chose already exists")
        if email_occupied:
            flash("This email is already used")
        if not passwords_match:
            flash("The passwords don't match")
        return redirect(url_for("signup")) # add flash messages
    else:
        return render_template("signup.html") 


@app.route('/login/', methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("profile"))
    if request.method == "POST":
        username = request.form["login"]
        user = User.query.filter_by(username=username).first()
        if user is not None:
            if request.form["password"] == user.password:
                session["user"] = user.username
                return redirect(url_for("profile"))
        else:
            flash("Password and login do not match")
        return redirect(url_for("login")) # flash messages
    else:
        return render_template("login.html")


@app.route('/logout/')
def logout():
    session.pop('user', None)
    return redirect(url_for("index"))


@app.route("/profile/")
def profile():
    if "user" in session:
        username = session["user"]
        user = User.query.filter_by(username=username).first()
        return render_template("profile.html", words=user.words)
    else:
        return "Not authorized"


if __name__ == "__main__":
    app.run(debug=True)
