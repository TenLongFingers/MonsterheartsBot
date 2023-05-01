## IMPORTS ##
import os
import discord
from discord.ext import commands
import string
from custom_modules.database_functions import fetch_characters_from_db, get_character_stats, add_new_character, delete_character_db

## DISCORD CLIENT INSTANCE ##
intents = discord.Intents.default()
intents.messages = True
intents.members = True

intents = discord.Intents.default()
intents.message_content = True

## VARIABLES ## TODO: after the name declaration, go back in and add all the help declarations in the arguments. name = "new_character", help = "Add new character"
bot = commands.Bot(command_prefix='!', intents=intents)
prefix = '!'


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
@bot.command(name='add_character')
async def new_character(ctx):
  #Get server ID from discord API
  server_id = ctx.guild.id

  #remove bot command
  input_string = ctx.message.content.lower().split()
  args = input_string[1:]
  args.append(str(server_id))
  #sanitize
  sanitized_character = "".join(ch for ch in " ".join(args)
                                if ch.isalnum() or ch.isspace() or ch == "-")

  # dictioanry for new character
  keys = [
    'first_name', 'last_name', 'skin', 'level', 'hot', 'cold', 'volatile',
    'dark', 'server_id'
  ]
  values = sanitized_character.split()

  new_character = {keys[i]: values[i] for i in range(len(keys))}

  new_character['first_name'] = new_character['first_name'].capitalize()
  new_character['last_name'] = new_character['last_name'].capitalize()
  new_character['skin'] = new_character['skin'].capitalize()
  new_character['level'] = int(new_character['level'])
  new_character['hot'] = int(new_character['hot'])
  new_character['cold'] = int(new_character['cold'])
  new_character['volatile'] = int(new_character['volatile'])
  new_character['dark'] = int(new_character['dark'])
  new_character['server_id'] = str(new_character['server_id'])

  #check to see if input is valid
  if len(args) != 9:
    await ctx.send(
      f"No new character has been made. Make sure you're putting it in the right order. \n Usage: {prefix}add_character <first name> <last name> <skin> <level> <hot> <cold> <volatile> <dark>. \n Note: if you are trying to add a new NPC, use {prefix}new_npc instead."
    )
    return

  result = (add_new_character(new_character))

  # Send new character as a confirmation message
  #TODO: actually include stat block TODO: add a more helpful error message
  if result:
    await ctx.send("success!")
  else:
    await ctx.send("fail")


@bot.command(name='character_list')
# Get server ID from Discord API
async def get_characters(ctx):

  # get server ID from discord
  server_id = ctx.guild.id

  characters = fetch_characters_from_db(server_id)

  if not characters.empty:
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

    await ctx.send("List of Player Characters: \n\n" + characters_string +
                   "\n *(note: to view npcs, use command " + prefix +
                   "get_npcs)*")
  else:
    await ctx.send("Failed to retrieve character data. Please try again later."
                   )


# see a single character's stats function TODO: for now I repeat the formatting. I'll consolidate that later, once I know everything works and I can isolate problems easier.
@bot.command(name='statblock')
async def stat_block(ctx):
  # get server ID from discord
  server_id = ctx.guild.id
  # extract name
  input_string = ctx.message.content.lower().split()
  name = ' '.join(input_string[1:]).capitalize()

  character = get_character_stats(name, server_id)

  if character is None:
    await ctx.send(
      f"Error: couldn't find {name} in character list. Did you spell it right? :thinking:"
    )
    return

  character_stats_message = (
    f"""**{character['first_name'].iloc[0]} {character['last_name'].iloc[0]}** *{character['skin'].iloc[0]}* (level {character['level'].iloc[0]})
            **Hot:** {character['hot'].iloc[0]}
            **Cold:** {character['cold'].iloc[0]}
            **Volatile:** {character['volatile'].iloc[0]}
            **Dark:** {character['dark'].iloc[0]}""")
  await ctx.send(character_stats_message)


# Delete character
@bot.command(name='delete_character')
async def delete_character(ctx):
  #get server_id
  server_id = ctx.guild.id
  #remove bot command
  input_string = ctx.message.content.lower().split()
  name = ' '.join(input_string[1:]).capitalize()

  if delete_character_db(name, server_id):
    await ctx.send(f'''{name} has been deleted from the character list.''')
  else:
    await ctx.send(f'''Error: {name} not found. No one's been deleted.''')


# #add conditions
@bot.command(name='add_conditon')
async def add_condition(ctx):
  #get server_id
  server_id = ctx.guild.id
  #remove bot command
  input_string = ctx.message.content.lower().split()
  args = input_string[1:]
  args.append(str(server_id))
  #sanitize
  sanitized_condition = "".join(ch for ch in " ".join(args)
                                if ch.isalnum() or ch.isspace())

  #dictionary for new condition
  keys = [
    'first_name'
  ]


# #hello message
# @bot.command(name='hello')
# async def hello(message):
#   await message.channel.send(
#     "Hello, world! This will eventually be updated with instructions on how to get instructions!"
#   )

#Rolling function

bot.run(os.getenv('TOKEN'))
