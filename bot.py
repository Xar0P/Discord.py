import discord
from discord.ext import commands

class Bot:

    def __init__(self, token) -> None:
        self.token = token


    def connect(self) -> discord:
        """ Returns a connection of bot """
        self.client = commands.Bot(command_prefix="x", case_insensitive = True, intents=discord.Intents.all())
        return self.client


    def run(self) -> None:
        """ Run the bot """
        self.client.run(self.token)