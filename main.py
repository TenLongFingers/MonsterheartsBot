## IMPORTS ##
import os
import discord
from discord.ext import commands
import string
from custom_modules.database_functions import get_characters, get_character_stats, add_new_character

## DISCORD CLIENT INSTANCE ##
intents = discord.Intents.default()
intents.messages = True
intents.members = True

intents = discord.Intents.default()
intents.message_content = True

## VARIABLES ##
bot = commands.Bot(command_prefix='!', intents=intents)


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
@bot.event
async def on_ready():
  print('We have logged in successfully as {0.user}'.format(bot))

# create new character function
@bot.command(name='new_character')
async def new_character(ctx, first_name, last_name, skin, level, hot, cold, volatile, dark):
  # Parse name, stat, and level arguments
  if not all(arg.isdigit() for arg in (level, hot, cold, volatile, dark)):
    await ctx.send("Usage: !new_character <first name> <last name> <skin> <level> <hot> <cold> <volatile> <dark>. \n Note: if you are trying to add a new NPC, use " + prefix + "new_npc instead.")
    return

  first_name = first_name.capitalize()
  last_name = last_name.capitalize()
  skin = skin.capitalize()
  level = int(level)
  hot = int(hot)
  cold = int(cold)
  volatile = int(volatile)
  dark = int(dark)

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
  await ctx.send("success!")

# Fetches the full list of player characters
@bot.command(name='get_characters')
async def get_characters(ctx):
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

  await ctx.send("List of Player Characters: \n\n" +
                 characters_string +
                 "\n *(note: to view npcs, use command " + prefix +
                 "get_npcs)*")

  # see a single character's stats function TODO: for now I repeat the formatting. I'll consolidate that later, once I know everything works and I can isolate problems easier. TODO: doesn't handle wrong names yet

@bot.command()
async def stat_block(ctx, *, name):
    character = get_character_stats(name)
    character_stats_message = (
        f"""**{character['first_name'].iloc[0]} {character['last_name'].iloc[0]}** *{character['skin'].iloc[0]}* (level {character['level'].iloc[0]})
            **Hot:** {character['hot'].iloc[0]}
            **Cold:** {character['cold'].iloc[0]}
            **Volatile:** {character['volatile'].iloc[0]}
            **Dark:** {character['dark'].iloc[0]}""")
    await ctx.send(character_stats_message)

@bot.command()
async def hello(ctx):
    await ctx.send("Hello, world! This will eventually be updated with instructions on how to get instructions!")



#Rolling function

bot.run(os.getenv('TOKEN'))
