from flask import Flask, request, render_template, redirect, flash
from helper import (
    get_basic_data, get_measures, get_evolution, 
    gather_weakness, index_pokemons, search_colors, format
    )

import random

# configure app
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Custom filter
app.jinja_env.filters["color"] = search_colors
app.jinja_env.filters["format"] = format

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
    
    # error checking
    if name:
        basic = get_basic_data(name)
        measures = get_measures(name)
        evolution = get_evolution(name)
        if basic != None and measures != None:
            return render_template('pokemon.html', basic=basic, measures=measures, evolution=evolution)
        else:
            flash(f'Invalid Pokémon name {name}')
    else:
        flash('Name cannot be empty')
    return redirect('/')