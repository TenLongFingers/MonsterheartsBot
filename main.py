## IMPORTS ##
import os
import discord
import random
from custom_modules.database_functions import get_characters, get_character_stats, add_new_character

## DISCORD CLIENT INSTANCE ##
intents = discord.Intents.default()
intents.messages = True
intents.members = True

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

## VARIABLES ##
prefix = "!"


class Character:

  def __init__(
    self,
    first_name,
    last_name,
    skin,
    level,
    hot,
    cold,
    volatile,
    dark,
  ):
    self.first_name = first_name
    self.last_name = last_name
    self.skin = skin
    self.level = level
    self.hot = hot
    self.cold = cold
    self.volatile = volatile
    self.dark = dark


# Check to see if the bot is logged in. Dev use only
@client.event
async def on_ready():
  print('We have logged in successfully as {0.user}'.format(client))


# create new character function TODO: build a function in the database_functions file so the new character will be inserted into the table
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  #shortens message content
  msg = message.content.lower()

  if msg.startswith(prefix + "new_character"):
    # parse name, stat, and level arguments
    args = msg.split()[1:]
    if len(args) != 8:
      await message.channel.send(
        "Usage: !new_character <first name> <last name> <skin> <level> <hot> <cold> <volatile> <dark>. **Remember not to use comas!** \n Note: if you are trying to add a new NPC, use "
        + prefix + "new_npc instead.")
      return

    else:
      # Extract values from args
      first_name = args[0]
      last_name = args[1]
      skin = args[2]
      level = int(args[3])
      hot = int(args[4])
      cold = int(args[5])
      volatile = int(args[6])
      dark = int(args[7])

      new_character = {
        'first_name': first_name,
        'last_name': last_name,
        'skin': skin,
        'level': level,
        'hot': hot,
        'cold': cold,
        'volatile': volatile,
        'dark': dark
      }
      add_new_character(new_character)
      print(new_character)
      # Send new character as a confirmation message #TODO: actually include stat block
      await message.channel.send("success!")

  # Fetches the full list of player characters
  if msg.startswith(prefix + "get_characters"):
    characters = get_characters()
    characters_list = []
    for index, character in characters.iterrows():
      character_info = (
        f"""**{character.first_name} {character.last_name}** *{character.skin}* (level {character.level})
          **Hot:** {character.hot}
          **Cold:** {character.cold}
          **Volatile:** {character.volatile}
          **Dark:** {character.dark}\n\n""")
      characters_list.append(character_info)
    characters_string = "\n".join(characters_list)

    await message.channel.send("List of Player Characters: \n\n" +
                               characters_string +
                               "\n \n (to view npcs, use command " + prefix +
                               "get_npcs")

  # see a single character's stats function TODO: for now I repeat the formatting. I'll consolidate that later, once I know everything works and I can isolate problems easier. TODO: doesn't handle wrong names yet
  if msg.startswith(prefix + "stat_block"):
    name = message.content[len(prefix + "stat_block"):].strip()
    character = get_character_stats(name)
    character_stats_message = (
      f"""**{character['first_name'].iloc[0]} {character['last_name'].iloc[0]}** *{character['skin'].iloc[0]}* (level {character['level'].iloc[0]})
          **Hot:** {character['hot'].iloc[0]}
          **Cold:** {character['cold'].iloc[0]}
          **Volatile:** {character['volatile'].iloc[0]}
          **Dark:** {character['dark'].iloc[0]}""")

    await message.channel.send(character_stats_message)

  # TODO: reformat this to have instructions
  if msg.startswith(prefix + "hello"):
    await message.channel.send(
      "Hello, world! This will eventually be updated with instructions on how to get instructions!"
    )


#Rolling function

client.run(os.getenv('TOKEN'))
