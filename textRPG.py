#!/usr/bin/python3
# Importing required libraries
import json
import os
import sys
import requests
import random

# Constant map:
direction_map = {
    "N": (0, 1, 0),
    "S": (0, -1, 0),
    "E": (1, 0, 0),
    "W": (-1, 0, 0),
    "NE": (1, 1, 0),
    "NW": (-1, 1, 0),
    "SE": (1, -1, 0),
    "SW": (-1, -1, 0),
    "U": (0, 0, 1),
    "D": (0, 0, -1)
}

# Function for calling LLM and returning a response.
def generate_response(prompts, max_tokens):

    url = "http://127.0.0.1:5000/api/v1/generate"

    headers = {
        "Content-Type": "application/json"
    }

    history = ""
    for prompt in prompts:
    
        # Create the prompt
        prompt = history + prompt
        
        # Create the request
        request = {
            'prompt': prompt,
            'max_new_tokens': max_tokens,
            'auto_max_new_tokens': False,
            'preset': 'simple-1'
        }

        # Debugging
        #print(f"\nPrompt: {prompt}\n")
        
        # Send the request
        temp_response = requests.post(url, headers=headers, json=request, verify=True)

        # Check for failure
        if temp_response.ok == False:
            result = f"Error: {temp_response.reason}"

        # Debugging
        #print(f"\nTemp Response JSON: {temp_response.json()}\n")
        result = temp_response.json()['results'][0]['text']
        
        # Build a history for applying the next prompt onto.
        # - I am not sure if this is needed, or if the connection keeps a history automatically.
        history = f"{prompt} {result} "
    
    return result

def random_seed():
    characters = "qwertyuiopasdfghjklzxcvbnm"
    length = 10
    random_string = ""
    for i in range(length):
        random_char = random.choice(characters)
        random_string += random_char
    random_string += " "
    return random_string

# Function to fix the classify text to fill in any valid variables.
def replace_variables(string, *args):
    for arg in args:
        string = string.format(**{k: v for k, v in arg.items() if k in string})
    return string
    
# Function to list all directories in a directory.
# - Used for displaying world names.
def list_dirs(path):
    if os.path.isdir(path):
        dirs = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path,name))]
        result = ", ".join(dirs)
        return result
    else:
        return ""

# Function for generating new worlds.
def create_world(world_name):
    file_path = f"worlds/{world_name}/settings.json"
    print(f"\nWorld: {world_name} : {file_path}\n")
    if not os.path.exists(file_path):
        response = input(f"Do you want to auto-generate a world setting [Y/n]? ").lower()
        if 'n' in response:
            world_settings = input(f"Describe in detail the game world / setting: ")
        else:
            classifier = load_classification_data()
            response = 'n' # Trigger a new response first time into the while loop.
            while True:
                if 'r' in response: pass
                elif 'n' in response:
                    params = input(f"Provide some parameters to help guide the generator if desired: ")
                    prompt = replace_variables(classifier['NewWorld'], {"input": params})
                else: break # Exit the while loop
                # Generating the output
                world_settings = generate_response([prompt], 200).strip()
                print(world_settings)
                response = input(f"[D]one, [r]egenerate, or [n]ew prompt? ").lower()
        save_world_settings(world_name, world_settings)
    else:
        print("World already exists!")
    
# Function to load player data from JSON file
def load_player_data(player_name):
    file_path = f"players/{player_name}.json"
    if not os.path.exists(file_path):
    
        # Code to create a new player.
        response = input(f"Character {player_name} not found. Do you want to make a new character? [Y/n] ")
        if 'n' in response.lower():
            sys.exit(1)

        player_data = {
            'location': ['none', 100, 100, 100],
            'description': 'A person',
            'items': 'none'
        }

        # Get the player's world.
        worlds = list_dirs("worlds")
        print(f"Worlds: {worlds}")
        world_name = input(f"Select a world or enter a new one: ")
        if world_name not in worlds:
            response = input("World doesn't exist. Make one? [Y/n] ").lower()
            if 'n' in response:
                print("Sure. Good Bye!")
                sys.exit(1)
            
            create_world(world_name)
            
        # Set the players start location (tries to avoid - numbers)
        player_data['location'] = [world_name, 100, 100, 100]
        
        # Get the players description:
        response = input(f"Do you want to auto-generate your character description [Y/n]? ").lower()
        if 'n' in response:
            description = input(f"Describe in detail your character: ")
        else:
            classifier = load_classification_data()
            world = load_world_settings(player_data['location'][0])
            response = 'n' # Trigger a new response first time into the while loop.
            while True:
                if 'r' in response: pass
                elif 'n' in response:
                    params = input(f"Provide some parameters to help guide the generator if desired: ")
                    prompt = replace_variables(classifier['NewCharacter'], {"world": world, "input": params, "name": player_name})
                else: break
                # Generating the output
                description = generate_response([prompt], 200).strip()
                print(description)
                response = input(f"[D]one, [r]egenerate, or [n]ew prompt?").lower()
        player_data['description'] = description
        save_player_data(player_data, player_name)
    else:
        with open(file_path, "r") as f:
            player_data = json.load(f)
    
    return player_data

# Function to save player data to JSON file
def save_player_data(player_data, player_name):
    if not os.path.exists("players"):
        os.makedirs("players")
    with open(f"players/{player_name}.json", "w") as f:
        json.dump(player_data, f)
    print("Player data saved.")

# Function to load location data from JSON file
def load_location_data(world, x, y, z, world_data):
    file_path = f"worlds/{world}/Z{z}/X{x}Y{y}.json"
    print (file_path)
    if not os.path.exists(file_path):
        dir_path = f"worlds/{world}/Z{z}"
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            
        # Code to create new location file using LLM model
        # - This is a new location:
        #   1. Check for neighboring locations?
        #   2. Info on connections?
        #   3. Where the player came from?
        # - For now we won't do any of that.
        location_data = {
            'title': '',
            'scene': '',
            'items': '',
            'actions': '',
            'directions': ''
        }
        
        # First: Describe the scene.
        print("Entering New Location - Starting Generation.")
        classifier = load_classification_data()
        response = 'n' # Trigger a new response first time into the while loop.
        while True:
            if 'r' in response: pass
            elif 'n' in response:
                params = input(f"Provide some parameters to help guide the generator if desired: ")
                if params == "": params = "None"
                prompt = replace_variables(classifier['NewScene'], {"world": world_data, "input": params})
            else: break
            # Generating the output
            description = generate_response([prompt], 400).strip()
            print(description)
            response = input(f"[D]one, [r]egenerate, or [n]ew prompt?").lower()
        location_data['scene'] = description

        # Second: Generate a title for this scene.
        response = 'r' # Trigger a new response first time into the while loop.
        prompt = replace_variables(classifier['SceneTitle'], {"scene": location_data['scene']})
        while True:
            if 'r' in response: pass
            else: break
            # Generating the output
            description = generate_response([prompt], 50).strip()
            print(description)
            response = input(f"[D]one, [r]egenerate?").lower()
        location_data['title'] = description

        # Third: Generate directions out of this scene.
        response = 'r' # Trigger a new response first time into the while loop.
        prompt = replace_variables(classifier['SceneDirections'], {"scene": location_data['scene']})
        while True:
            if 'r' in response: pass
            else: break
            # Generating the output
            description = generate_response([prompt], 100).strip()
            print(description)
            response = input(f"[D]one, [r]egenerate?").lower()
        location_data['directions'] = description

        # Forth: Generate actions in this scene.
        response = 'r' # Trigger a new response first time into the while loop.
        prompt = replace_variables(classifier['SceneActions'], {"scene": location_data['scene']})
        while True:
            if 'r' in response: pass
            else: break
            # Generating the output
            description = generate_response([prompt], 100).strip()
            print(description)
            response = input(f"[D]one, [r]egenerate?").lower()
        location_data['actions'] = description

        # Fifth: Generate items in this scene.
        # - Broke the response generator into 2 posts.
        # - I was unable to get a consistant valid response with only one.
        # - The first post identifies the items and the second lists them.
        response = 'r' # Trigger a new response first time into the while loop.
        if isinstance(classifier['SceneItems'], str): classifier['SceneItems'] = [classifier['SceneItems']]
        prompts = [replace_variables(item, {"scene": location_data['scene']}) for item in classifier['SceneItems']]
        while True:
            if 'r' in response: pass
            else: break
            # Generating the output
            description = generate_response(prompts, 100).strip()
            print(description)
            response = input(f"[D]one, [r]egenerate?").lower()
        location_data['items'] = description

        # Update the old location with any changes.
        save_location_data(location_data, world, x, y, z)
        
    else:
        with open(file_path, "r") as f:
            location_data = json.load(f)

    return location_data

# Function to save location data to JSON file
def save_location_data(location_data, world, x, y, z):
    if not os.path.exists(f"worlds/{world}/Z{z}"):
        os.makedirs(f"worlds/{world}/Z{z}")
    file_path = f"worlds/{world}/Z{z}/X{x}Y{y}.json"
    with open(file_path, "w") as f:
        json.dump(location_data, f)

# Function to load classification data from JSON file
# - This is kept seperate so that the classifiers can be massaged as needed 
#   without having to change this code.
def load_classification_data():
    file_path = f"classification.json"
    if not os.path.exists(file_path):
        print(f"{file_path} not loaded.")
        sys.exit(1)
    with open(file_path, "r") as f:
        classification_data = json.load(f)
    return classification_data

# Function to load world settings from JSON file
# - The world settings are used by the location generator and response
#   classifiers to help guide the game generation and responses.
def load_world_settings(world):
    file_path = f"worlds/{world}/settings.json"
    if not os.path.exists(file_path):
        print(f"{file_path} not loaded.")
        sys.exit(1)
    with open(file_path, "r") as f:
        world_settings = json.load(f)
    return world_settings

# Function to save world data to JSON file
def save_world_settings(world, world_settings):
    if not os.path.exists(f"worlds/{world}"):
        os.makedirs(f"worlds/{world}")
    file_path = f"worlds/{world}/settings.json"
    with open(file_path, "w") as f:
        json.dump(world_settings, f)

# Function to get user input
def get_user_input():
    print("")
    player_input = input("Enter your command: ")
    return player_input

# Function to print scene output
# TODO: Provide alternate output destinations.
def print_scene_title(location_data):
    print(location_data["title"])

# Function to print scene output
# TODO: Provide alternate output destinations.
def print_scene_output(location_data):
    print(f"\n{location_data['scene']}")

# Function to print local items output
# TODO: Provide alternate output destinations.
def print_local_items_output(location_data):
    print(f"\nItems in the location: {location_data['items']}")

# Function to print actions output
# TODO: Provide alternate output destinations.
def print_actions_output(location_data):
    print(f"\nAvailable actions: {location_data['actions']}")

# Function to classify text adventure game inputs
def classify_input(classifier, type, *args):

    prompt = replace_variables(classifier[type]['prompt'], *args)

    # Generating the classification output
    category = generate_response([prompt], 10).strip()

    # If the category is invalid, send a retry request to the LLM
    responses = replace_variables(classifier[type]['responses'])
    if category not in responses:
        prompt = replace_variables(classifier['Retry'], {'responses': responses})

        # Generating the classification output
        category = generate_response([prompt], 10).strip()

    if category not in responses:
        category = ''
        
    # Returning the category
    return category

# Function to generate a natural language response.
def natural_response(classifier, type, *args):
    
    new_prompt = replace_variables(classifier[type], *args)

    # Generating the response output
    print(generate_response([new_prompt], 1999).strip())

# Function for moving the player
# -args 3 is currently the player data. (FIX?)
def player_moving(classification_data, *args):
    global direction_map
    # Re-Classify user input
    direction = classify_input(classification_data, 'Moving', *args)

    # Getting direction coordinates
    if direction in direction_map:

        # Getting current location 
        world, x, y, z = args[3]["location"]
        dx, dy, dz = direction_map[direction]
        
        # Update the old location with any changes.
        save_location_data(args[2], world, x, y, z)

        # Updating player location (move the player)
        args[3]["location"] = [world, x + dx, y + dy, z + dz]
        return

    # Invalid direction specified. Give a natural response.
    natural_response(classification_data['InvalidDirection'], *args)

# Function for processing commands
def player_command(classification_data, player_name, *args):

    # Re-Classify user input
    action = classify_input(classification_data, 'Action', *args)

    # Checking if player wants to quit or save
    if action == "quit":
        # Exiting the game loop
        save_player_data(args[3], player_name)
        sys.exit(1)
    elif action == "save":
        # Saving player data
        save_player_data(args[3], player_name)
    #else:
        # Invalid command specified. Give a natural response.
         #natural_response(classification_data['InvalidCommand'], *args)

# Main function
def main():
    # Getting player name
    player_name = input("Enter your name: ")

    # Loading player data
    player_data = load_player_data(player_name)

    # Loading world settings
    world_settings = load_world_settings(player_data["location"][0])

    # Loading classification data
    classification_data = load_classification_data()
    
    # Game loop
    while True:

        # Loading location data
        location_data = load_location_data(*player_data["location"], world_settings)

        # Printing scene title
        print_scene_title(location_data)

        # Printing scene output
        print_scene_output(location_data)

        # Printing local items output
        print_local_items_output(location_data)

        # Printing actions output
        print_actions_output(location_data)

        # Getting user input
        player_input = get_user_input()

        # Roll all the variables and stuff that an LLM would need to process info into a dictonary.
        # - This will be used to substitute {} variables with game data.
        # - There are probably better ways to do this.
        valid_params = {
            "world": world_settings, 
            "scene": location_data['scene'],
            "items": location_data['items'],
            "actions": location_data['actions'],
            "directions": location_data['directions'],
            "name": player_name,
            "player": player_data['description'],
            "inventory": player_data['items'],
            "input": player_input
        }

        # Classifying user input into 4 main category types: Using Something, Moving, Entering a Command, or None of the above.
        # - This may be changed later to add or move categories around.
        # - This is used to focus the players response into one type and hopefully provide better analysis and control of the input.
        category = classify_input(classification_data, 'InputType', valid_params)

        # Processing user input based on category
        if category == "1":
            # Using or interacting with an item they have or in the location
            natural_response(classification_data, 'Use', valid_params)
        elif category == "2":
            # Moving
            player_moving(classification_data, valid_params)
        elif category == "3":
            # Trying to use a common command like quit, save
            player_command(classification_data, player_name, valid_params)
        else:
            # Doing something not allowed
            natural_response(classification_data, 'NaturalRequest', valid_params)

# Starting the game
if __name__ == "__main__":
    main()
