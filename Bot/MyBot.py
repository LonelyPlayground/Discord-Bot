import sys
import os
import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import *
from Token.Token import *
from Erik_Quotes.quote import *
import datetime
#API refrence sheet - http://discordpy.readthedocs.io/en/latest/api.html#client
#bot commands framework https://discordpy.readthedocs.io/en/rewrite/ext/commands/commands.html

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

#Github documentation for gspread-https://github.com/burnash/gspread
#Good video explaining sheets API - https://www.youtube.com/watch?v=vISRn5qFrkM
#needed installs - pip install gspread oauth2client

Client = discord.Client()
bot_prefix = "#"
client = commands.Bot(command_prefix = bot_prefix)
myToken = Token()
token = myToken.getToken()
eQuotes = Quote()
aQuotes = eQuotes.getQuotes
today = datetime.datetime.now()

#sheets api stuff
scope = ['http://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
clients = gspread.authorize(creds)
sheet = clients.open_by_url('https://docs.google.com/spreadsheets/d/1tXI_ZYpqUoIuKiPrE4A5UzDKbSTpkw1BvvXf7RU1ofI/edit#gid=0').sheet1
pp = pprint.PrettyPrinter()

#prints in command line to show that the bot is online
@client.event
async def on_ready():
	print("Bot Online!")
	print("Name: " + client.user.name)
	print("ID: " + client.user.id)
	print("We have logged in as {0.user}".format(client))

#@client.event
#async def on_message(message):
#    if message.author == client.user:
#        return
#    if message.content.startswith('#hello'):
#        await message.channel.send('Hello!')



#responds with "pong" when a user types ping
#@client.event
#async def on_message(message):
	#if message.content.startswith('#hi '):
#	user = ctx.message.author.id
#	await client.send_message(message.author,"Hi, <@%s>"%(user,))


@client.command(pass_context=True)
async def hi(ctx):
	print("test")
	authorid = ctx.message.author.id
	await client.say("Hi, <@%s>"%authorid)

@client.command(pass_context=True)
async def ping(ctx):
	await client.say("Pong!")

#test, says thinking emoji
@client.command(pass_context=True)
async def memes(ctx):
	await client.say(":thinking:")

#responds with a random Erik quote
@client.command(pass_context=True)
async def quote(ctx):
	sQuote = eQuotes.getRandQuote()
	if sQuote['Date'] == "":
		sQuote['Date'] = "Date Unkown"
	await client.say(sQuote['Quote'] + " -" + sQuote['Who'] + " (%s)"%sQuote['Date'])

#allows uses to add to a google spread sheet and get a random quote
#TODO: add error handling and explain usage
@client.command(pass_context=True)
async def add_quote(ctx, arg1, arg2, *args):
	if len(args) == 0:
		arg3 = str(today.month) + "/" + str(today.day) + "/" + str(today.strftime("%y"))
		await client.say("No date given so defaulted to today (%s)"%arg3)
	else:
		arg3 = args[0]
	row = [arg1, arg2, arg3]
	sheet.append_row(row, value_input_option='USER_ENTERED')
	await client.say("Quote added by <@%s>"%ctx.message.author.id)

#TODO have a data base of users and a balence, then allow them to gamble by making a session and having them roll, then having the lowest roll pay the difference to the highest roll.
@client.command(pass_context=True)
async def gamble(ctx):
	await client.say("TODO, Contact <@102910284225593344> or other contributers and make him get to work!")

#runs client
client.run(token)