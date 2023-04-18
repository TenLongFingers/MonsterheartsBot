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


# Check to see if the bot is logged in. Developer use only
@client.event
async def on_ready():
  print('We have logged in successfully as {0.user}'.format(client))


# Dice roller function
@client.event
async def roll_dice():
  dice_1 = random.randint(1, 6)
  dice_2 = random.randint(1, 6)
  total = dice_1 + dice_2
  return total, dice_1, dice_2


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content

  # TODO: reformat this to have instructions
  if msg.startswith("!hello"):
    await message.channel.send(
      "Hello, world! This will eventually be updated with instructions on how to get instructions!"
    )

  if msg.startswith("!roll"):
    total, dice_1, dice_2 = await roll_dice()
    await message.channel.send("You rolled " + str(dice_1) + " and " +
                               str(dice_2) + " for a total of " + str(total))


client.run(os.getenv('TOKEN'))
