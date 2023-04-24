import random
from main import prefix, msg

exclamations_array = [
  "WOW!", "HOLY SH*T!", "F*CK YEAH!", "HOT DAMN!", "ya-YEET!", "POG!", "(⊙０⊙)",
  "ᕦ༼ ˵ ◯ ਊ ◯ ˵ ༽ᕤ"
]


## FUNCTIONS##
# Dice roller function TODO: add the stats as a callback function. Then you can do an if/elif statements in the roll function, so they can choose whether or not to roll stats
def roll_dice():
  dice_1 = random.randint(1, 6)
  dice_2 = random.randint(1, 6)
  total = dice_1 + dice_2
  return total, dice_1, dice_2

#Rolling function


# Random exclamations for super successes
  exclamation = random.choice(exclamations_array)
  if msg.startswith(prefix + "roll"):
    total, dice_1, dice_2 = roll_dice()
    result = "You rolled " + str(dice_1) + " and " + str(
      dice_2) + " for a total of " + str(total)

    # Messages for different rolls TODO: these will probably have to be moved to a different function so people can add stats. It'll have to be restructured.
  if total == 2:
    result = (":poop:  ") + result + ("! FAIL!")
  elif 3 <= total <= 6:
    result = ("Fail! ") + result + (".")
  elif 7 <= total <= 9:
    result = ("Success! ") + result + (".")
  elif total > 9:
    result = (exclamation + " " + result + ("! SUCCESS!!"))
  await message.channel.send(result)

