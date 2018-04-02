import discord
from discord.ext.commands import Bot
from discord.ext import commands
from Token.Token import *
from Erik_Quotes.quote import *
#API refrence sheet - http://discordpy.readthedocs.io/en/latest/api.html#client
#bot commands framework https://discordpy.readthedocs.io/en/rewrite/ext/commands/commands.html
Client = discord.Client()
bot_prefix = "#"
client = commands.Bot(command_prefix = bot_prefix)
myToken = Token()
token = myToken.getToken()
eQuote = Quote()
#Something
#prints in command line to show that the bot is online
@client.event
async def on_ready():
	print("Bot Online!")
	print("Name: " + client.user.name)
	print("ID: " + client.user.id)
#responds with "pong" when a user types ping
@client.command(pass_context = True)
async def ping(ctx):
	await client.say("Pong!")
#test, says thinking emoji
@client.command(pass_context = True)
async def memes(ctx):
	await client.say(":thinking:")
#responds with a random Erik quote
@client.command(pass_context = True)
async def quote(ctx):
	newQuote = eQuote.getQuote()
	await client.say(newQuote)
#TODO: save quotes in a spread sheet and allow users to add to it
@client.command(pass_context = True)
async def add_quote(ctx):
	await client.say("TODO, Contact <@101444971701207040> or other contributers and make him get to work!")
#TODO have a data base of users and a balence, then allow them to gamble by making a session and having them roll, then having the lowest roll pay the difference to the highest roll.
@client.command(pass_context = True)
async def gamble(ctx):
	await client.say("TODO, Contact <@102910284225593344> or other contributers and make him get to work!")
#runs client
client.run(token)