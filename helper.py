import requests
import random
import asyncio
import httpx


TYPES = {}
COLOR_SCHEME = {
    "Normal": "#A8A77A",
    "Fire": "#EE8130",
    "Water": "#6390F0",
    "Electric": "#F7D02C",
    "Grass": "#7AC74C",
    "Ice": "#96D9D6",
    "Fighting": "#C22E28",
    "Poison": "#A33EA1",
    "Ground": "#E2BF65",
    "Flying": "#A98FF3",
    "Psychic": "#F95587",
    "Bug": "#A6B91A",
    "Rock": "#B6A136",
    "Ghost": "#735797",
    "Dragon": "#6F35FC",
    "Steel": "#B7B7CE",
    "Dark": "#705746",
    "Fairy": "#D685AD"
}


# ordering neccessary data
def pokemon_details(name):
    try:
        # getting data from api
        pokemon_data = lookup(f'pokemon/{name.lower()}')

        # getting pokemon species
        species = pokemon_data['species']['name']

        # getting species data
        species_data = lookup(f'pokemon-species/{species}')

        # getting evolutionary chain
        evol_url = species_data['evolution_chain']['url'].replace('https://pokeapi.co/api/v2/', '')
        evo_data = lookup(evol_url)

        # getting pokemon abilities
        abilities = [ability['ability']['name'].capitalize() for ability in pokemon_data['abilities']]

        # getting pokemon moves
        moves = [move['move']['name'].capitalize() for move in pokemon_data['moves']]
        
        # getting types
        types = [t['type']['name'].capitalize() for t in pokemon_data['types']]
        
        # converting height into feet and inches
        height = format(0, pokemon_data['height'])

        # converting weight into pounds
        weight = format(1, pokemon_data['weight'])

        # formatting the pokemon id
        id = format(2, pokemon_data['id'])
        
        # search for weakness
        weakness = search_weakness(types)
        
        # getting flavour texts
        flavours = []
        for flv_text in species_data['flavor_text_entries']:
            if flv_text['language']['name'] == 'en':
                flavours.append(flv_text['flavor_text'])

        # getting evolution chain
        evoloution = []
        current_link = evo_data['chain']
        while current_link:
            evoloution.append(current_link['species']['name'].capitalize())

            if current_link.get('evolves_to') and len(current_link.get('evolves_to')) > 0:
                current_link = current_link['evolves_to'][0]
            else:
                current_link = None

        return {
            'id': id,
            'name': pokemon_data['name'].capitalize(),
            'norm-img-url': pokemon_data['sprites']['other']['official-artwork']['front_default'],
            'shiny-img-url': pokemon_data['sprites']['other']['official-artwork']['front_shiny'],
            'height': height,
            'weight': weight,
            'abilities': abilities,
            'moves': moves,
            'types': types,
            'weakness': weakness,
            'evolution': evoloution,
            'flavours': flavours
        }
    
    except Exception as e:
        print(e)
    
    return None


# get images and details of index page pokemons
def index_pokemons():
    ids = []
    for _ in range(6):
        ids.append(random.randint(1, 1025))

    return asyncio.run(syncronize_request(ids))


async def get_pokemon_data(client, id):
    resp = await client.get(f"https://pokeapi.co/api/v2/pokemon/{id}")
    data = resp.json()
    return [data['id'], data['name'], data['sprites']['other']['official-artwork']['front_default'], [t['type']['name'].capitalize() for t in data['types']]]


async def syncronize_request(ids):
    async with httpx.AsyncClient() as client:
        tasks = [get_pokemon_data(client, id) for id in ids]
        return await asyncio.gather(*tasks)


# requesting data from pokeapi
def lookup(path):
    url = f"https://pokeapi.co/api/v2/{path}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        return data
    except Exception as e:
        print(e)
    
    return None


# search for weakness
def search_weakness(types):
    array = []

    for type in types:
        for i in TYPES[type]:
            if i.capitalize() not in types:
                array.append(i.capitalize())
    
    return sorted(array)

# search for color types
def search_colors(type):
    return COLOR_SCHEME[type]


# gathering weakness of each pokemon type
def gather_weakness():
    for i in range(1, 20):
        data = lookup(f'type/{i}')
        for item in data['names']:
            if item['language']['name'] == 'en':
                name = item['name']
    
        array = []
        for item in data['damage_relations']['double_damage_from']:
            array.append(item['name'])

        TYPES[name] = array


# format numbers
def format(type, number):
    if type == 0:
        number = str(round(((number / 10) * 39.37) / 12, 1))
        n1 = int(number.split('.')[0])
        n2 = int(number.split('.')[1][:1])
        return f"{n1}' " + f'{n2:02}"'
    
    elif type == 1:
        number = str(round((number / 10) * 2.20462, 1))
        return f'{number} lbs'

    elif type == 2:
        return f'#{number:04}'