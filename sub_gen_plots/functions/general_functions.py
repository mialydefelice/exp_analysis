from datetime import date
import os

def get_todays_date():
	"""
	Want to grab today's date so that data in output folders is not 
	overwritten (just in case its needed later)
	"""
	today = date.today()
	month = str(today.month)
	if len(month) < 2:
		month = '0' + str(today.month)
	date_str = month + str(today.day) + str(today.year)[2:]
	return date_str

def make_output_directory(path):
	if not os.path.exists(path):
		os.makedirs(path)
		return