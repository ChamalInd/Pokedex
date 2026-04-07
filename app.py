from flask import Flask, request, render_template, redirect, flash, session
from flask_session import Session

# configure app
app = Flask(__name__)

# configure main route
app.route('/')
def index():
    flash("Hello World")
    return render_template('index.html')