import requests
import random


TYPES = {}


# ordering neccessary data
def pokemon_details(name):
    try:
        # getting data from api
        name = str(name)
        if name.isnumeric():
            pokemon_data = lookup(f'pokemon/{name}')
        else:
            pokemon_data = lookup(f'pokemon/{name.lower()}')
        species = pokemon_data['species']['name']
        species_data = lookup(f'pokemon-species/{species}')
        evol_url = species_data['evolution_chain']['url'].replace('https://pokeapi.co/api/v2/', '')
        evo_data = lookup(evol_url)

        # getting pokemon abilities
        abilities = make_array(pokemon_data, 'abilities', 'ability')

        # getting pokemon moves
        moves = make_array(pokemon_data, 'moves', 'move')
        
        # getting types
        types = make_array(pokemon_data, 'types', 'type')
        
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
    data_array = []
    i = 0

    while i < 6:
        try:
            data = pokemon_details(random.randint(1, 1025))
            data_array.append([data['id'], data['name'], data['norm-img-url'], data['types']])
            i += 1
        except Exception as e:
            print(e)

    return data_array


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


# making required arrays 
def make_array(data, category_type, ctegory_name):
    array = []
    for item in data[category_type]:
            array.append(item[ctegory_name]['name'].capitalize())
    
    return array


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