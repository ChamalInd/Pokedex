from flask import Flask, request, render_template, redirect, flash, session
from flask_session import Session
from helper import pokemon_details, gather_weakness, index_pokemons

# configure app
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# gather weakness of all pokemons at the begining
gather_weakness()


@app.after_request
def after_request(response):
    # Ensure responses aren't cached
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# configure main route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('action') == 'refresh':
           pokemons = index_pokemons()

    pokemons = index_pokemons()
    return render_template('index.html', pokemons=pokemons)

@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    name = request.form.get('name')
    data = pokemon_details(name)
    return render_template('pokemon.html', data=data)