import requests
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, session, url_for

with open("key.txt") as f:
    API_KEY = f.read()
SEARCH_VOLUME = "https://www.googleapis.com/books/v1/volumes?q=search+terms"
SEARCH_URL = "https://www.googleapis.com/books/v1/volumes"

app = Flask(__name__)
app.secret_key = "awer7qwctnxeilqOAGFKS"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, name, password):
        self.name = name
        self.password = password


@app.route('/',  methods=["POST", "GET"])
def index():
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            query = request.form["query"]
            response = requests.get(SEARCH_URL, params={"q": query, "appid": API_KEY})
            books = response.json()["items"]
            print(books)
            return render_template('index.html', username=user, books=books)
        else:
            pass
        return render_template('index.html', username=user)
    else:
        return render_template('index.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["username"]
        password = request.form["password"]
        if "login" in request.form:
            found_user = Users.query.filter_by(name=user).first()
            if found_user:
                if found_user.password == password:
                    session["user"] = user
                    session["password"] = password
                    return redirect(url_for("index"))
                else:
                    return render_template("login.html", login_failed=True)
            else:
                return render_template("login.html", user_not_found=True)
        else:
            session["user"] = user
            session["password"] = password
            usr = Users(user, password)
            db.session.add(usr)
            db.session.commit()
            return redirect(url_for("index"))
    else:
        return render_template("login.html")


@app.route('/book/<book_id>')
def book_info(book_id):
    response = requests.get(f'{SEARCH_URL}/{book_id}')
    book = response.json()
    return render_template('book_info.html', book_info=book)


@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for('index'))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)