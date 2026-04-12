# PokéDex
#### Vide Demo: https://youtu.be/5hIkzvLd6DA
#### Project: https://github.com/ChamalInd/Pokedex.git


### Project Overview

A Simple and Interactive Pokédex inspired by the PokéDex on Pokémon website. <br>
You can view it by clicking [here](https://www.pokemon.com/us/pokedex)

### Features
- Can view pokemon's details (Name, Physical Measure, Abilities, ...)
- Can add your favourite pokemons
- Can view evolutionary chain of pokemons
- Interactive UI

### Tech Stack
- Back End: Python 3.4, Flask
- Front End: HTML, CSS, BootStrap 5
- Database: SQLite3
- APIs: [PokéApi](https://pokeapi.co)

### Project Structure
- `app.py`: The main controller containing all Flask routes and backend logic
- `helper.py`: Utility functions for reqesting data from api and formating them
- `pokedex.db`: Database containing program data
- `requirements.txt`: File containing all the required python libreries
- `static/`
    - `style.css`: Contain all the styles of the website
    - `pokeball.png`: Website logo
- `templates/`
    - `layout.html`: The base template containing basic UI
    - `index.html`: The html file for the index page
    - `pokemon.html`: The html file to view pokemon data
    - `favourites.html`: The html file to view favourites


### Getting Started

#### Prerequisites
- Make sure you have Python installed. <br>
    You can check by running ```python --vesion```
- Make sure you have SQLite3 installed. <br>
    You can check by running ```sqlite3 --vesion```

#### Installation
- Clone the project to your system
    ```
    git clone
    cd pokedex
    ```
- Then install all the requirements
    ```
    pip install -r requirement.txt
    ```

#### Running the App
- Run `Flask run` on your terminal to and click the link provided to view the website.

### Future Improvements
- Add User Login to make the user feel more interactive
- Implement different themes for user's preference
