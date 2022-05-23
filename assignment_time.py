import argparse
import urllib.request
from bs4 import BeautifulSoup
import json
import pandas as pd

def get_timezone():
'''
Returns the timezone in a readable format given the json url
'''
	url='https://raw.githubusercontent.com/dmfilipenko/timezones.json/master/timezones.json'
	try:
		result=urllib.request.urlopen(url)
	except urllib.error.URLError as en:
		print('Unable to fetch timezones. Connection Error.')
		exit(0)
	timezones = result.read()
	soup = BeautifulSoup(timezones, features="html.parser")
	return json.loads(soup.text)

if __name__=="__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--match', type=str, default=None)
	parser.add_argument('--offset', type=float, default=None)
	args = parser.parse_args()
	print(f'Arguements recieved are: {args}')

	time_zones = get_timezone()

	offset_res = []
	if args.offset:
		for i in time_zones:
			if args.offset == i['offset']:
				offset_res.append(i)
		if not offset_res:
			print(f'No timezone found for this offset: {args.offset}')
			exit(0)
	time_zones = offset_res if offset_res else time_zones	

	output = []
	if args.match:
		match = args.match.lower()
		for i in time_zones:
			if match in i['value'].lower():
				output.append(i)
		if not output:
			print(f'No timezone found for this match: {match}')
			exit(0)
	else:
		output = time_zones
	df = pd.DataFrame(output)
	print(df.to_string())

