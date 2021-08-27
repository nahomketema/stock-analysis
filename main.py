#!/usr/bin/env python3

'''
Nahom Ketema
main.py

This is the file where everything comes together. All routes are defined here.
Note that if you delete the database(.db file), you'll need to come up with another unique name or the program might act unexpectedly(on line 32)
'''

from os import system
import requests
import secrets
from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from flask_behind_proxy import FlaskBehindProxy
# Local imports below
from forms import RegistrationForm, LoginForm, SearchForm
from api import search_tickers, recent_value, generate_graph, twitter_search_hashtag, sentiment_analysis

# Flask app and global values declared below
app = Flask(__name__)
proxied = FlaskBehindProxy(app)
bcrypt = Bcrypt(app)
secret_key=secrets.token_hex(16)
app.config["SECRET_KEY"] = secret_key
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
login_status = False
login_name = "" # value gets set as "" if logged out
searchinfo = {
    "name": "",
    "ticker": ""
}

# Database related code below
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site_data.db"
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(30), nullable=False)
    def __repr__(self):
        return f"User('{self.username}','{self.email}')"
class Save(db.Model): #Since the apis being used are fairly lineant, only the ticker symbol is needed to save the data
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    tickername = db.Column(db.String(20), nullable=False)
    def __repr__(self):
        pass

db.create_all()

#web routes below
@app.route("/")
def home():
    return render_template("home.html", login_status=login_status)

@app.route("/register", methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if(form.validate_on_submit()):
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        )
        try:
            db.session.add(user)
            db.session.commit()
        except exc.IntegrityError:
            flash("The username is already taken. Please try again")
        else:
            flash(f"Account created for {form.username.data}!", "success")
            global login_status
            login_status = True
            global login_name
            login_name = form.username.data
        finally:
            return redirect(url_for("home"))
    return render_template("register.html", login_status=login_status, form=form)

@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm()
    if(form.validate_on_submit()):
        user = db.session.query(User).filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                flash("Logged in successfully!", category="success")

                global login_status
                login_status=True
                global login_name
                login_name=form.username.data
                return redirect(url_for("home"))
            else:
                flash("Incorrect password, try again.", category="error")
                return redirect(url_for("login"))
        else:
            flash("User name does not exist", category="error")
            return redirect(url_for("login"))
    return render_template("login.html", login_status=login_status, form=form)

@app.route("/logout")
def logout():
    global login_status
    login_status = False
    global login_name
    login_name = ""
    return redirect(url_for("home"))

@app.route("/search", methods=["GET", "POST"])
def search():
    form = SearchForm()
    if(form.validate_on_submit()):
        global searchinfo
        searchinfo["name"] = form.searchname.data
        searchinfo["ticker"] = form.tickername.data
        return redirect(url_for("results"))
    return render_template("search.html", login_status=login_status, form=form)

@app.route("/search/results")
def results():
    #once search gets used up, the search variable is reset
    global searchinfo
    matches = search_tickers(searchinfo["name"])
    if(searchinfo["ticker"] != ""):
        filtered_matches = []
        length = len(matches)
        counter = 0
        while(counter < length):
            if(matches[counter]["ticker symbol"].lower() == searchinfo["ticker"]):
                filtered_matches.append(matches[counter].copy()) #might behave unexpectedly if we don't include the .copy()
            counter += 1
        matches = filtered_matches
    searchinfo["name"] = "" #gets reset once it gets used
    searchinfo["ticker"] = ""
    return render_template("search_results.html", login_status=login_status, login_name=login_name, matches=matches)

@app.route("/search/results/<ticker>")
def more_info(ticker):
    # Here, the graph gets generated and then it gets embedded into more_information.html
    generate_graph(recent_value(ticker))#this generates and stores a graph as an html file
    recent_tweets = twitter_search_hashtag(ticker)
    if(recent_tweets == []):
        return render_template("more_information.html", login_status=login_status, login_name=login_name, ticker=ticker, recent_tweets=[], sentiment_score=0)
    sentiment_score = 0
    count = 0
    for tweet in recent_tweets:
        sentiment_score += sentiment_analysis(tweet)
        count += 1
    try:
        average = sentiment_score/count #impossible to get a divide by zero error but playing it safe
    except Exception as e:
        print("An error happened. Code: ", e)
        average = 0
    return render_template("more_information.html", login_status=login_status, login_name=login_name, ticker=ticker, recent_tweets=recent_tweets, sentiment_score=average)

@app.route("/save/<ticker>")
def save():
    if(login_status == False):
        pass
    return redirect(url_for("saved"))

@app.route("/saved")
def saved():
    #content here
    return render_template("saved.html", login_status=login_status, login_name=login_name)

@app.route("/about")
def about():
    return render_template("about.html", login_status=login_status, login_name=login_name)

if (__name__ == "__main__"):
    app.run(debug=True)
