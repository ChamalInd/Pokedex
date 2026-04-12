from flask import Flask, request, render_template, redirect, flash
from helper import (
    get_basic_data, get_measures, get_evolution, 
    gather_weakness, index_pokemons, search_colors,
    format, syncronize_request, get_pokemon_names
)

import sqlite3
import asyncio

# configure app
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# configuring database
con = sqlite3.connect("pokedex.db", check_same_thread=False)
cursor = con.cursor()

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

    names = get_pokemon_names()
    pokemons = index_pokemons()
    return render_template('index.html', pokemons=pokemons, names=names)


@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    name = request.form.get('name')
    
    # error checking
    if name:
        basic = get_basic_data(name)

        if basic:
            measures = get_measures(name)
            evolution = get_evolution(name)

            favs = cursor.execute('SELECT * FROM favourites').fetchall()
            for i in favs:
                if basic["id"] == i[0]:
                    isfav = True
                    break
                else:
                    isfav = False

            return render_template('pokemon.html', basic=basic, measures=measures, evolution=evolution, isfav=isfav)
        else:
            flash(f'Invalid Pokémon name {name}')
    else:
        flash('Name cannot be empty')
    return redirect('/')


@app.route('/favourites', methods=['POST'])
def show_favourites():
    favs = cursor.execute('SELECT * FROM favourites').fetchall()
    ids = []
    for i in favs:
        ids.append(i[0])
    data = asyncio.run(syncronize_request(ids))
    print(data)
    return render_template('favourites.html', pokemons=data)


@app.route('/set-favourites', methods=['POST'])
def set_favourite():
    if request.method == 'POST':
        id = int(request.form.get('id'))

        favs = cursor.execute('SELECT * FROM favourites').fetchall()

        for i in favs:
            if id == i[0]:
                isfav = True
                break
            else:
                isfav = False

        if not isfav:
            cursor.execute('INSERT INTO favourites (id) VALUES(?)', (id, ))
            con.commit()
            flash('Successfully added Pokémon to the Favourites.')
        else:
            cursor.execute('DELETE FROM favourites WHERE id = ?', (id, ))
            con.commit()
            flash('Successfully removed Pokémon from the Favourites.')
        return redirect('/')