# LLM_Text_Adventure_Generator
LLM Text Adventure Generator

## Description
This is a 'Text Adventure Game' and Generator. Designed to look and feel like the old text adventure games and MUDs. A scene is described, and the player enters their action.

Behind the game is an LLM communication system currently designed to work with 'oobabooga' [https://github.com/oobabooga/text-generation-webui]. It will:
1. Take the users input, which can be natural or gamified.
2. Check it against a list of possible actions.
3. Process the action if it is a valid game action.
4. Respond to the user natually.

There are are two main modes: Game and Generator.
1. Game mode - The player can move through the game envirnment, do actions, etc.
2. Generator Mode - If a scene that isn't generated yet by an LLM is encountered a new scene will be generated.

## Goal
I have three goals for this project.
1. Learning - Develop my skills with LLM game development and python programming.
2. Gaming - Eventually have a game engine to play with.
3. Provide - A building block, and/or game for others to develop on and play with.

## Files
* textRPG.py - The main game engine. This could possibly be broken up into multiple files, each with their own part of the game engine. But I am new to this, and didn't really put a full plan into place on the final structure. Eventually I may refactor this if it needs it.
* classification.json - This has the LLM prompts to send to oobabooga (or eventually other GPTs). The name on this file probably should change. It was originally designed to hold my classifier that was processing my game engine 'commands'. But it has changed into holding all the formatted text to send to the LLM. The goal of this file is to seperate the game logic from the LLM requests. This way if another model is loaded that needs the requests formatted differently, it can easily be swapped out. Also it makes it easier to update the requests as needed to provide better, more accurate responses.

## Others
While developing this code I eventually thought; I wonder if anyone else is making something simular. So here is a list of other LLM Text Adventure Games. I may eventually review these others for insperation if I get stuck, but I want to try to write this entirely on my own.

If you are making your own and want me to link it here feel free make a comment with the path to the game. I will add it to this list. Or notify me if you want it removed from this list:
* AdventureGPT: [https://github.com/oaguy1/AdventureGPT]
* GPT Adventure Game Engine: [https://github.com/nferraz/gpt-adventures]
