# External Packages
import os
import discord
import random
from dotenv import load_dotenv

# Local Files
import utils

# Create the bot
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

# My list of compliments. %user% is to be replaced with the user's name
compliments = ["You look nice today %user%!", "Are those your real teeth %user%?", "Did you fall from heaven %user%, because you look like an angel?"]

# Task 12
cat_photo_folder = "cat_photos"
cat_list = []
for filename in os.listdir(cat_photo_folder):
    cat_list.append(filename)


def generate_compliment(username):
    """Returns a random compliment to a specific user"""
    response = random.choice(compliments)
    response = response.replace("%user%", username)
    return response


@client.event
async def on_ready():
    # Triggered when starting up the bot
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_member_update(before, after):
    if str(before.status) == "offline" and str(after.status) == "online":
        # When a user comes online
        channel = utils.get_channel_by_name(client, after.guild, 'general')
        try:
            # Tasks 5 and 6
            compliment = generate_compliment(after.name)
            response = f"Hello {after.name}. {compliment}"
            await channel.send(response)
        except discord.errors.Forbidden:
            pass


@client.event
async def on_message(message):
    if message.author == client.user:
        # Ignore messages this bot sends
        return

    current_channel = message.channel

    if message.content and len(message.content) > 1 and message.content[0] == '!':
        # First we extract the message after the ! then split it on spaces to
        # get a list or the arguments the user gave
        message_text = message.content[1:]
        split_message = message_text.split(" ")
        command = split_message[0]

        if command == "test":
            response = "test successful"
            await current_channel.send(response)
        elif command == "hello":
            # Tasks 1 and 2
            response = f"Hello {message.author.mention}!"
            await current_channel.send(response)
        elif command == "compliment":
            # Tasks 3 and 4
            response = generate_compliment(message.author.mention)
            await current_channel.send(response)
        elif command == "guess":
            # Tasks 7 and 8
            my_guess = random.randint(1, 100)
            response = ""
            if len(split_message) > 1:
                try:
                    user_guess = int(split_message[1])
                    if user_guess == my_guess:
                        response = "Correct!"
                    elif user_guess < 1 or user_guess > 100:
                        # Task 9
                        response = f"Wrong, sorry! You guessed {user_guess} but that is not between 1 and 100!"
                    else:
                        response = f"Wrong, sorry! You guessed {user_guess} but I was thinking of {my_guess}"
                except ValueError:
                    response = f"Does \"{split_message[1]}\" look like a whole number to you?"
            else:
                response = "You didn't enter a guess!"
            await current_channel.send(response)
        elif command == "meow":
            # Tasks 10 and 11
            filename = os.path.join(cat_photo_folder, random.choice(cat_list))
            my_file = discord.File(filename)
            await current_channel.send(file=my_file)

client.run(TOKEN)
