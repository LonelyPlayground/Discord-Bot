from random import *
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

scope = ['http://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1tXI_ZYpqUoIuKiPrE4A5UzDKbSTpkw1BvvXf7RU1ofI/edit#gid=0').sheet1

class Quote:
	def __init__(self):

		self.quotes = sheet.get_all_records(empty2zero=False, head=1, default_blank='')

	def getRandQuote(self):
		rowcount = len(self.quotes)
		return self.quotes[randint(0, (rowcount - 1))]

	def getQuotes(self):
		return self.quotes