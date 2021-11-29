#!/usr/bin/python3.9.7
import sys
import requests
import json
import csv
import datetime

def fetch_version_and_time(packageName):
	URL='https://registry.npmjs.org/'
	r = requests.get(URL+packageName)


	if r.status_code == 200:
		print('[fetching {}] success'.format(packageName))
		data = r.json()
		last_version = data['dist-tags']["latest"]
		time = data['time']['modified']
		return (last_version, time)

def write_to_output(rows):
	HEADER=["name", "current version", "last version", "need update ?", "last update time", "outdated more than a year"]

	with open("result.csv", 'w') as f:
		writer = csv.writer(f)

		writer.writerow(HEADER)
		for row in rows:
			if len(row) == len(HEADER):
				writer.writerow(row)

def read_input_package_json(filename):
	current_date = datetime.date.today()
	print('[reading] start')

	with open(filename, 'r') as f:
		print('[reading] success')

		data = json.load(f)

		dependencies = data['dependencies']
		packages = dependencies.keys()

		data=[]

		for count, packageName in enumerate(packages, start=1):
			print('[fetching {}] {}/{}'.format(packageName, count, len(packages)))
			(last_version, time) = fetch_version_and_time(packageName)

			current_version=dependencies[packageName][1:]

			duration = current_date - datetime.date.fromisoformat(time[:10])
			data.append([packageName, current_version, last_version, current_version != last_version, f'years: {int(duration.days/365)} days: {duration.days}', int(duration.days/365) > 1])

		write_to_output(data)

read_input_package_json(sys.argv[1])
