from flask import Blueprint, session, request
from flask_restful import Api, Resource
from database import User, Word, RepDate, db


class WordStorer(Resource):

    def get(self):
        if "user" in session:
            username = session["user"]
            user = User.query.filter_by(username=username).first()
            return user.words, 200
        else:
            return {"result": "Success", "description": "Not authorized"}, 401

    def post(self):
        if "user" in session:
            username = session["user"]
            user = User.query.filter_by(username=username).first()
            word = request.form["word"]
            if word not in list(map(lambda word: word.word, user.words)):
                new_word = Word(word=word, user=user)
                user.words.append(new_word)
                db.session.add(user)    
                db.session.commit()
                return {"result": "Success", "description": "The word has been added", "word": word, "wordId": new_word.id}, 200
            else:
                return {"result": "Failure", "description": "Can not add the same word twice"}, 200
        else:
            return {"result": "Failure", "description": "Not authorized"}, 401

    def delete(self, word_id):
        if "user" in session:
            username = session["user"]
            user = User.query.filter_by(username=username).first()
            print(type(user.words))
            db.session.delete(Word.query.filter_by(id=word_id).first())
            db.session.commit()
            return {"result": "Success", "description": "The word has been removed"}, 200
        else:
            return {"result": "Failure", "description": "Not authorized"}, 401


class WordUpdater(Resource):

    def post(self, word_id):
        if "user" in session:
            username = session["user"]
            user = User.query.filter_by(username=username).first()
            try:
                user.words[word_id].dates.append(RepDate())
                db.session.add(user)
                db.session.commit()
                return {"result": "Success", "description": "Successfully added the repdate"}, 200
            except:
                return {"result": "Failure", "description": "The word with such id does not exist"}, 200
        else:
            return {"result": "Failure", "description": "Not authorized"}, 401


api_blueprint = Blueprint("api_blueprint", __name__)
api = Api(api_blueprint)
api.add_resource(WordStorer, "/", "/<int:word_id>")
api.add_resource(WordUpdater, "/update-word/<int:word_id>")
