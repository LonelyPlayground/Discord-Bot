import sys
import os
import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import *
from Token.Token import *
from Erik_Quotes.quote import *
from Gambling.gambling import *
from Gambling.gamblingHelpers import rollFunc, activeSessions
import datetime

#API refrence sheet - http://discordpy.readthedocs.io/en/latest/api.html#client
#bot commands framework https://discordpy.readthedocs.io/en/rewrite/ext/commands/commands.html

import gspread
from oauth2client.service_account import ServiceAccountCredentials

#Github documentation for gspread-https://github.com/burnash/gspread
#Good video explaining sheets API - https://www.youtube.com/watch?v=vISRn5qFrkM
#needed installs - pip install gspread oauth2client

#this is from the Discord API and it is the setup that is required for the bot to run
Client = discord.Client()
bot_prefix = "#"
client = commands.Bot(command_prefix = bot_prefix)
myToken = Token()
token = myToken.getToken()
eQuotes = Quote()
aQuotes = eQuotes.getQuotes #not currently used

today = datetime.datetime.now() #this uses the datetime library to make a variable that is today's date
error = "" #this is a variable that is used in the add_quote function to keep track of what is formatted incorrectly

#This is the setup that us needed for the google sheets API including a client id for the project and a link to the google sheet
scope = ['http://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
clients = gspread.authorize(creds)
sheet = clients.open_by_url('https://docs.google.com/spreadsheets/d/1tXI_ZYpqUoIuKiPrE4A5UzDKbSTpkw1BvvXf7RU1ofI/edit#gid=0').sheet1

#function to check if date is formated correctly
def checkDate(date):
	datelist = date.split("/")
	print(datelist)
	try:
		i = int(datelist[0])
	except:
		return "Month must be numbers"
	try:
		i = int(datelist[1])
	except:
		return "Day must be numbers"
	try:
		i = int(datelist[2])
	except:
		return "Year must be numbers"
	if int(datelist[0]) > 12 or int(datelist[0]) < 1:
		return "Invalid month"
	elif int(datelist[1]) > 31 or int(datelist[1]) < 1:
		return "Invalid day"
	elif int(datelist[2]) > 99 or int(datelist[2]) < 0:
		return "Invalid year"
	return "no error"

#This is from the Discord API and it prints info about the bot on startup to make sure it is working

@client.event
async def on_ready():
	print("Bot Online!")
	print("Name: " + client.user.name)
	print("We have logged in as {0.user}".format(client))

#allows uses to add to a google spread sheet and get a random quote
#all @client.command, @client.event, and ascync function lines use the discord API
#what is contained in each function is what I wrote using the some functions from the API like client.say
#The API is used to call the function but I wrote the algorthm of the function
@client.command(pass_context=True)
async def add_quote(ctx, *args):
	global error
	global date
	try:
		if len(args) < 2 or len(args) > 3:
			error = "Invalid Usage"
			await client.say("Error: " + error)#client.say is a discord API function that prints to the discord chat
			print(error)
			pass
		elif not(args[1].isalpha()):
			error = "Invalid name"
			await client.say("Error: " + error)#Discord API
			print(error)
			pass
		elif len(args) == 2:
			date = str(today.month) + "/" + str(today.day) + "/" + str(today.strftime("%y"))#uses the datatime library to format today's date
			await client.say("No date given so defaulted to today (%s)"%date)
		else:
			date = args[2]
		if error == "":
			error = checkDate(date)
			if not(error == "no error"):
				await client.say("Error: " + error)#Discord API
	except:
		await client.say("Usage: #add_quote <“quote within quotation marks”> <who said it> <date(mm/dd/yy)>")#Discord API
		await client.say("Date is optional, if no value is given it will use today's date.")#Discord API
		print("error passed")
		error = "error passed"
	finally:
		if error == "no error":
			quote = "“%s”"%args[0]
			name = args[1].lower()
			name = name.capitalize()
			row = [quote, name, date]
			sheet.append_row(row, value_input_option='USER_ENTERED')#google sheets api that appends a row to the google sheet.
			eQuotes.__init__()
			await client.say("Quote added by <@%s>, see it here: https://docs.google.com/spreadsheets/d/1tXI_ZYpqUoIuKiPrE4A5UzDKbSTpkw1BvvXf7RU1ofI/edit#gid=0"%ctx.message.author.id)#Discord API
		elif error == "error passed":
			pass
		else:
			await client.say("Usage: #add_quote <“quote within quotation marks”> <who said it> <date(mm/dd/yy)>")#discord API
			await client.say("Date is optional, if no value is given it will use today's date.")#Discord API

#responds with a random quote
@client.command(pass_context=True)
async def quote(ctx):
	sQuote = eQuotes.getRandQuote()
	if sQuote['Date'] == "":
		sQuote['Date'] = "Date Unkown"
	await client.say(sQuote['Quote'] + " -" + sQuote['Who'] + " (%s)"%sQuote['Date'])



#these three function are very simple function I wrote when testing and learning the Discord API
@client.command(pass_context=True)
async def hi(ctx):
	print("test")
	authorid = ctx.message.author.id
	await client.say("Hi, <@%s>"%authorid)

@client.command(pass_context=True)
async def ping(ctx):
	await client.say("Pong!")

#simple command to test the bot API, says thinking emoji
@client.command(pass_context=True)
async def memes(ctx):
	await client.say(":thinking:")
  
@client.command(pass_context = True)
async def roll(ctx, *args):
	rolled = rollFunc(args, ctx.message.author.id)
	await client.say(rolled)
#TODO have a data base of users and a balence, then allow them to gamble by making a session and having them roll, then having the lowest roll pay the difference to the highest roll.
@client.command(pass_context = True)
async def gamble(ctx, *args):
	house = Gamble()
	start = house.gambleStart(args, ctx.message.author.id)
	await client.say(start)
@client.command(pass_context = True)
async def join(ctx, *args):
	global activeSessions
	if not len(args) == 1:
		await client.say("Usage: #join <sessionID>")
	else:
		try:
			await client.say(activeSessions[int(args[0])].join(ctx.message.author.id))
		except:
			await client.say("No active session at this ID")
@client.command(pass_context = True)
async def start_roll(ctx, *args):
	global activeSessions
	if not len(args) == 1:
		await client.say("Usage: #start_roll <sessionID>")
	else:
		try:
			await client.say(activeSessions[int(args[0])].start_roll())
		except:
			await client.say("No active session at this ID")

#runs client using Discord API
client.run(token)