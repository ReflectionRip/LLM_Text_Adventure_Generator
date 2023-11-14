# LLM_Text_Adventure_Generator
An LLM Text Adventure Game and Generator to provide it's players with endless entertainment.

## Description
This is a 'Text Adventure Game' and Generator. Designed to look and feel like the old text adventure games and MUDs. A scene is described, and the player enters their action.

Behind the game is an LLM communication system currently designed to work with 'oobabooga' [oobabooga Text generation web UI](https://github.com/oobabooga/text-generation-webui). It will:
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

## To Do
This is a general list of goals. I will probably add to it as new goals are discovered, and remove from it as old goals are completed.
* Get the basic functionality working.
* Implement a better movement system with areas, regons and/or zoning.
* Gradio to provide the users with a web-based Interface.
* Generation Rating/Voting system. When the LLM generates a scene or other descriptive text I was thinking it may be cool to allow it to generate multiple versions, and let the user rate/vote on what version is the best. Or just rate an LLM generated response on a scale or nauturally, guiding the LLM to improve it's responses.
* Tracking system - Inventory / Scene changes / Goals
* Streamed output - When generating LLM responses, the outputs will take time to generate. Stream the outputs from the LLM. When loading pre-generated outputs (already generated scenes, inventories, etc) the outout will be nearly instantaneous. Implement a streaming system for loaded outputs. \[Enable/Disable\] 
* Stable Diffusion - Text to Image - Generation for scenes / items. \[Enable/Disable\]
* TTS - Text to Speach - Allow the users to listen instead of read. \[Enable/Disable\]
* STT? - Speach to Text - Allow the users to talk instead of type. \[Enable/Disabme\]
* \[Stretch Goal\] Multi-user support - MUD - Allow multiple players in one game session. \[Optional\]
* \[Stretch Goal\] Database? - This will probably be needed if MUD support is implemented.


## Others
While developing this code I eventually thought; I wonder if anyone else is making something simular. So here is a list of other LLM Text Adventure Games. I may eventually review these others for insperation if I get stuck, but I want to try to write this entirely on my own.

If you are making your own and want me to link it here feel free make a comment with the path to the game. I will add it to this list. Or notify me if you want it removed from this list:
* [oaguy1 AdventureGPT](https://github.com/oaguy1/AdventureGPT)
* [nferraz GPT Adventure Game Engine](https://github.com/nferraz/gpt-adventures)
