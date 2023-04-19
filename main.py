import os
import discord
import random

my_secret = os.environ['TOKEN']

intents = discord.Intents.default()
intents.messages = True
intents.members = True

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
prefix = "!"

exclamations_array = [
  "WOW!", "HOLY SH*T!", "F*CK YEAH!", "HOT DAMN!", "ya-YEET!", "POG!", "(⊙０⊙)",
  "ᕦ༼ ˵ ◯ ਊ ◯ ˵ ༽ᕤ"
]


# Check to see if the bot is logged in. Developer use only
@client.event
async def on_ready():
  print('We have logged in successfully as {0.user}'.format(client))


# Dice roller function TODO: add the stats as a callback function. Then you can do an if/elif statements in the roll function, so they can choose whether or not to roll stats
@client.event
async def roll_dice():
  dice_1 = random.randint(1, 6)
  dice_2 = random.randint(1, 6)
  total = dice_1 + dice_2
  return total, dice_1, dice_2


# Random exclamations for super successes
exclamation = random.choice(exclamations_array)


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  # TODO: reformat this to have instructions
  if msg.startswith(prefix + "hello"):
    await message.channel.send(
      "Hello, world! This will eventually be updated with instructions on how to get instructions!"
    )

  #Rolls a simple 2d6
  if msg.startswith(prefix + "roll"):
    total, dice_1, dice_2 = await roll_dice()
    result = "You rolled " + str(dice_1) + " and " + str(
      dice_2) + " for a total of " + str(total)
    # Messages for different rolls TODO: these will probably have to be moved to a different function so people can add stats. It'll have to be restructured.
    if total == 2:
      result = (":poop: ... ") + result + ("! FAIL!")
    elif 3 <= total <= 6:
      result = ("Fail! ") + result + (".")
    elif 7 <= total <= 9:
      result = ("Success! ") + result + (".")
    elif total > 9:
      result = (exclamation + " " + result + ("! SUCCESS!!"))
    await message.channel.send(result)


client.run(os.getenv('TOKEN'))
