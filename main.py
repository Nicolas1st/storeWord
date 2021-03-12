from flask import Flask, render_template, request, redirect, url_for, session
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
        return render_template("profile.html", words=list(map(lambda word: word.word, user.words)))
    else:
        return "Not authorized"


# class WordManager(Resource):

#     def get(self, word_id=None, date=None):

#         if "user" in session:
#             login = session["user"]
#             user = User.query.filter_by(login=login).first()
#             if word_id is not None:
#                 return list(map(lambda word: word.word, user.words))[word_id]
#             elif date is not None:
#                 # year, month, day = date.split("-")
#                 date = date(*date.split("-"))
#                 return list(filter(lambda word: word.date_found == date, user.words))
#                 # return user.words.filter_by(date_found=date)
#             else:
#                 return list(map(lambda word: word.word, user.words))
                
#         #     if word_id is None:             
#         #         return words
#         #     else:
#         #         return list(filter(lambda word: word.id == word_id, words))[0]
#         # else:
#         #     abort(401)
#         # else:
#         #     if "words" not in session:
#         #         session["words"] = []
#         #     if word_id is not None:
#         #         return session["words"][word_id]
#         #     if date is not None:
#         #         pass    
#         #     return session["words"]
                
#     def post(self):
#         word = request.form["word"]
#         if "user" in session:
#             user = User.query.filter_by(login=session["user"]).first()
#             if word not in list(map(lambda word: word.word, user.words)):
#                 word = Word(word=word, user_id=user.id)    
#                 user.words.append(word)
#                 db.session.add(user)
#                 db.session.commit()
#                 return {"result": "Success"}
#             else:
#                 return {"result": "Failure"}
#         else:
#             if "words" not in session:
#                 session["words"] = []
#             if word not in session["words"]:
#                 session["words"] += [word]
#                 return {"result": "Success"}
#             else:
#                 return {"result": "Failure"}

#     def delete(self, word_id):
#         pass

#     def patch(self):
#         pass
        


# api.add_resource(WordManager, "/words/", "/words/<int:word_id>", "/words/<string:date>")

if __name__ == "__main__":
    app.run(debug=True)
