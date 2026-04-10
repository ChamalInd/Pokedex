from flask import Flask, request, render_template, redirect, flash
from helper import (
    get_basic_data, get_measures, get_types_weakness, get_facts_moves, get_evolution, 
    gather_weakness, index_pokemons, search_colors
    )

import random

# configure app
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Custom filter
app.jinja_env.filters["color"] = search_colors

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


@app.route('/pokemon-basics', methods=['GET', 'POST'])
def pokemon_basics():
    name = request.form.get('name')
    
    # error checking
    if name:
        basic = get_basic_data(name)
        measures = get_measures(name)
        if basic != None and measures != None:
            # fact_num = random.randint(0, len(data['flavours']))
            return render_template('basics.html', basic=basic, measures=measures)
        else:
            flash(f'Invalid Pokémon name {name}')
    else:
        flash('Name cannot be empty')
    return redirect('/')


@app.route('/pokemon-tacticts', methods=['GET', 'POST'])
def pokemon_tacticts():
    name = request.form.get('name')
    
    # error checking
    if name:
        basic = get_basic_data(name)
        moves = get_facts_moves(name)
        if basic != None and moves != None:
            fact_num = random.randint(0, len(moves['flavours']))
            return render_template('facts-moves.html', basic=basic, moves=moves, fact_num=fact_num)
        else:
            flash(f'Invalid Pokémon name {name}')
    else:
        flash('Name cannot be empty')
    return redirect('/')


@app.route('/pokemon-evolution', methods=['GET', 'POST'])
def pokemon_evolution():
    name = request.form.get('name')
    
    # error checking
    if name:
        basic = get_basic_data(name)
        moves = get_facts_moves(name)
        if basic != None and moves != None:
            fact_num = random.randint(0, len(moves['flavours']))
            return render_template('facts-moves.html', basic=basic, moves=moves, fact_num=fact_num)
        else:
            flash(f'Invalid Pokémon name {name}')
    else:
        flash('Name cannot be empty')
    return redirect('/')