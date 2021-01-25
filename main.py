from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    words = db.relationship("Word", lazy="select", backref=db.backref("user", lazy="joined"))


class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(40), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    


db.create_all()

words = []


@app.route('/', methods=["GET", "POST"])
def index():
    user = User.query.filter_by(username="username").first()
    if request.method == "POST":
        word = Word(word=request.form["word"], user_id=user.id)
        user.words.append(word)
        db.session.add(user)
        db.session.commit() 
    return render_template("index.html", words=list(map(lambda word: word.word, user.words)))


if __name__ == "__main__":
    user = User(username="username")
    db.session.add(user)
    db.session.commit()
    # word = Word(word="NewlyRecordedWord", user_id=user.id)
    app.run(debug=True)
