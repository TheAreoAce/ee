import os
import discord
from keep_alive import keep_alive
from discord.ext import commands
import cmd

prefixes = ["/", "!"]  # List of prefixes you want to use

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or(*prefixes),
    case_insensitive=True
)

bot.author_id = 966495665096110130  # Change to your discord id!!!

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier

cmd.setup(bot)

extensions = [
    'cogs.cog_example'  # Same name as it would be if you were importing it
]

if __name__ == '__main__':  # Ensures this is the file being ran
    for extension in extensions:
        bot.load_extension(extension)  # Loads every extension.

keep_alive()  # Starts a webserver to be pinged.
token = os.environ.get("token")
bot.run(token)  # Starts the bot
