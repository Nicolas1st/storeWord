from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.secret_key = "secrethelloworldkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    words = db.relationship("Word", lazy="select", backref=db.backref("user", lazy="joined"))


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False)
    date_found = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    

db.create_all()


@app.route('/', methods=["GET", "POST"])
def index():
    return render_template("index.html", words=list(map(lambda user: user.login, User.query.all())))


@app.route('/signup/', methods=["GET", "POST"])
def signup():
    if "user" in session:
        return redirect(url_for("profile"))
    if request.method == "POST":
        user_exists = User.query.filter_by(login=request.form["login"]).first()
        email_occupied = User.query.filter_by(email=request.form["email"]).first()
        passwords_match = request.form["password"] == request.form["repeated_password"]
        if not user_exists and not email_occupied and passwords_match:
            new_user = User(login=request.form["login"],
                            email=request.form["email"],
                            password=request.form["password"])
            db.session.add(new_user)
            db.session.commit()
            session["user"] = new_user.login
            return redirect(url_for("profile"))
        return redirect(url_for("signup"))
    else:
        return render_template("signup.html")


@app.route('/login/', methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("profile"))
    if request.method == "POST":
        user = User.query.filter_by(login=request.form["login"]).first()
        if user is not None:
            if request.form["password"] == user.password:
                session["user"] = user.login
                return redirect(url_for("profile"))
        else:
            return redirect(url_for("login"))
    else:
        return render_template("login.html")


@app.route('/logout/')
def logout():
    session.pop('user', None)
    return redirect(url_for("index"))


@app.route("/profile/", methods=["GET", "POST"])
def profile():
    if "user" not in session:
        return redirect(url_for("login"))
    user = User.query.filter_by(login=session["user"]).first()
    if request.method == "POST":
        word = request.form["word"]
        if word not in list(map(lambda word: word.word, user.words)):
            word = Word(word=word, user_id=user.id)
            user.words.append(word)
            db.session.add(user)
            db.session.commit()
    return render_template("profile.html", words=list(map(lambda word: word.word, user.words)))


if __name__ == "__main__":
    app.run(debug=True)
