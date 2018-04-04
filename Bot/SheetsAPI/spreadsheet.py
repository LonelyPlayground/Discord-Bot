import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

#Github documentation for gspread-https://github.com/burnash/gspread
#Good video explaining sheets API - https://www.youtube.com/watch?v=vISRn5qFrkM
#needed installs - pip install gspread oauth2client

scope = ['http://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1tXI_ZYpqUoIuKiPrE4A5UzDKbSTpkw1BvvXf7RU1ofI/edit#gid=0').sheet1

pp = pprint.PrettyPrinter()

#result = sheet.cell(2,2).value
#pp.pprint(result)
#sheet.update_cell(2,2, 'Brandon')

sheet.delete_row(4)