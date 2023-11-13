# Importing required libraries
import json
import os
import sys
import requests

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
def generate_response(prompt, max_tokens):

    url = "http://127.0.0.1:5000/v1/completions"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "prompt": prompt,
        "max_tokens": max_tokens,
        "temperature": 1,
        "top_p": 0.9
    }

    temp_response = requests.post(url, headers=headers, json=data, verify=False)
    response = temp_response.json()['choices'][0]['text']
    return response

# Function to fix the classify text to fill in any valid variables.
def replace_variables(string, *args):
    for arg in args:
        string = string.format(**{k: v for k, v in arg.items() if k in string})
    return string
    
# Function to load player data from JSON file
def load_player_data(player_name):
    file_path = f"players/{player_name}.json"
    if not os.path.exists(file_path):
    
        # Code to create a new player.
    
        pass
    else:
        with open(file_path, "r") as f:
            player_data = json.load(f)
    
    return player_data

# Function to save player data to JSON file
def save_player_data(player_data, player_name):
    with open(f"players/{player_name}.json", "w") as f:
        json.dump(player_data, f)
    print("Player data saved.")

# Function to load location data from JSON file
def load_location_data(world, x, y, z, world_data):
    file_path = f"worlds/{world}/Z{z}/X{x}Y{y}.json"
    if not os.path.exists(file_path):
    
        # Code to create new location file using LLM model

        pass
    else:
        with open(file_path, "r") as f:
            location_data = json.load(f)

    return location_data

# Function to save location data to JSON file
def save_location_data(location_data, world, x, y, z):
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
    print(f"\Items in the location: {location_data['items']}")

# Function to print actions output
# TODO: Provide alternate output destinations.
def print_actions_output(location_data):
    print(f"\nAvailable actions: {location_data['actions']}")

# Function to classify text adventure game inputs
def classify_input(classifier, type, *args):

    prompt = replace_variables(classifier[type]['prompt'], *args)

    # Generating the classification output
    category = generate_response(prompt, 10).strip()

    # If the category is invalid, send a retry request to the LLM
    responses = replace_variables(classifier[type]['responses'])
    if category not in responses:
        prompt = replace_variables(classifier['Retry'], {'responses': responses})

        # Generating the classification output
        category = generate_response(prompt, 10).strip()

    if category not in responses:
        category = ''
        
    # Returning the category
    return category

# Function to generate a natural language response.
def natural_response(classifier, type, *args):
    
    new_prompt = replace_variables(classifier[type], *args)

    # Generating the response output
    print(generate_response(new_prompt, 1999).strip())

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
    else:
        # Invalid direction specified. Give a natural response.
        natural_response(classification_data['InvalidCommand'], *args)

# Main function
def main():
    # Getting player name
    player_name = input("Enter your name: ")

    # Loading player data
    player_data = load_player_data(player_name)

    # Loading world settings
    world_settings = load_world_settings(player_data["location"]["world"])

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
