from flask import Flask, render_template, request, redirect, url_for, session
from flask_restful import Api, Resource
from database import *



app = Flask(__name__)
app.secret_key = "secrethelloworldkey"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db.init_app(app)


with app.app_context():
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


@app.route("/profile/")
def profile():
    if "user" in session:
        user = User.query.filter_by(login=session["user"]).first()
        return render_template("profile.html", words=list(map(lambda word: word.word, user.words)))
    else:
        return render_template("profile.html", words=words["session"])


api = Api(app)


class WordManager(Resource):

    def get(self, word=None):
        if word in None:
            if "user" in session:
                login = session["user"]
                User.query.filter_by(login=login).first()
                words=list(map(lambda word: word.word, user.words)))
                return words
            else:
                return session["words"]
        else:
            # planning to return statistics about this word on get, but its not yet implemented
            return word

    def post(self, word):
        if "user" in session:
            user = User.query.filter_by(login=session["user"]).first()
            if word not in list(map(lambda word: word.word, user.words)):
                word = Word(word=word, user_id=user.id)    
                user.words.append(word)
                db.session.add(user)
                db.session.commit()
                return {"result": "The word has been added"}
            else:
                return {"result": "Cannot add the same word twice"}
        else:
            if word not in session["words"]:
                session["words"] += [word]
                return {"result": "The word has been added"}
            else:
                return {"result": "Cannot add the same word twice"}



api.add_resource(WordManager, "word/<string:word>")

if __name__ == "__main__":
    app.run(debug=True)
