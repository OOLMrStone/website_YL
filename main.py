import requests
from flask import Flask, render_template, request, redirect, session, url_for

API_KEY = "AIzaSyBKsbCBq3_QuSbRu8uv5Aj-MxtVacoH6lQ"
SEARCH_VOLUME = "https://www.googleapis.com/books/v1/volumes?q=search+terms"
SEARCH_URL = "https://www.googleapis.com/books/v1/volumes"

app = Flask(__name__)
app.secret_key = "awer7qwctnxeilqOAGFKS"


@app.route('/',  methods=["POST", "GET"])
def index():
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            query = request.form["query"]
            response = requests.get(SEARCH_URL, params={"q": query, "appid": API_KEY})
            print(response.text)
            return render_template('index.html', username=user, book=response.status_code == 200)
        else:
            pass
        return render_template('index.html', username=user)
    else:
        return render_template('index.html')


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        if "login" in request.form:
            pass
        else:
            user = request.form["username"]
            password = request.form["password"]
            session["user"] = user
            session["password"] = password
            return redirect(url_for("index"))
    else:
        return render_template("login.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)