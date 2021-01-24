## Instructions to run
`pip install -r requirements.txt`

`python main.py`
## Inspiration
Everyone knows the fastest way to learn a language is to live in a society that speaks the language. Conventional apps and websites used to learn a language take lots of time and practice compared to learning through experiences. In The Rosetta Throne, you can learn the language by doing 'real world' quests, and have fun playing a video game while you learn.
## What it does
The player begins in a unique procedurally generated environment. All text in the game is in the player’s chosen language including GUI elements and the pause menu. The player’s goal is to level up by completing quests for NPCs. They have to do this by figuring out what the NPCs want interacting with them and learning what their quests are through trial and error. The game also features all custom art made during the hackathon.
## How we built it
The world of the game is generated procedurally and extends as far as the player moves. It is made up of biomes, with temperature gradients, and chunks such as deserts, grasslands, savannahs, tundras, and forests. Each biome has its own texture and foliage density, and is populated by objects as well, including bushes, rocks, cacti, and different types of trees. Other things generated procedurally include towns, rivers, bridges, roads, and NPC’s. Towns contain branching roads and houses on them, with several NPC’s and objects such as chests or barrels. These NPC’s can be interacted with to complete quests, and the chests and barrels can be searched for items. Rivers, roads, and bridges are present as well, with roads turning into bridges over the rivers allowing the player to walk them instead of swimming.
## Challenges we ran into
Perlin noise and procedural generation are hard to get right, and making the landscape look visually pleasing was difficult. The translation API used also had a rate-limit which locked us out after too many requests, leading us to learn how to cache the results.
## Accomplishments that we're proud of
A fully functioning game and infinite world that you can explore. The world generation is not simply random, but gradual (ie deserts are not next to forest regions, instead, deserts slowly change to savannah, then to grassland, then to forest)
## What we learned
Lots about procedural generation and basic game design
## What's next for The Rosetta Throne
We would love to add more complexity to the world (biome types, quests, plants, npcs, etc...), multiplayer (to chat with real people in the language you are learning), and someday even publish the game to Steam.
