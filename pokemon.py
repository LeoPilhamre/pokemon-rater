import requests

import json


class utils():
	def GET(self, url):
		return requests.get(url)


	def toJSON(self, data):
		return data.json()


	def storeJSON(self, path, data):
		with open(path, 'w') as f:
			json.dump(data, f, indent=4)


class main(utils):
	def __init__(self):
		self.baseURL = 'https://pokeapi.co/api/v2/pokemon/'

		self.settings = {
			'limit': 100
		}


		self.data = {}


		self.count = self.getCount()


		self.call()


		self.storeJSON('data.json', self.data)



	def call(self):
		rest = self.count % self.settings['limit']

		n = int((self.count - rest) / self.settings['limit'])
		for i in range(n):
			data = self.getData((i + 1) * self.settings['limit'])

			results = data['results']

			for result in results:
				name = result['name']
				url = result['url']

				print(name, url)

				self.data[name] = self.scrapePokemonData(url)


	def getData(self, offset):
		data = self.GET(f"{self.baseURL}?offset={offset}&limit={self.settings['limit']}")

		json = self.toJSON(data)

		return json


	def getCount(self):
		data = self.GET(self.baseURL)

		json = self.toJSON(data)

		return json['count']


	def scrapePokemonData(self, url):
		data = self.getPokemonData(url)

		image = data['sprites']['other']['official-artwork']['front_default']
		height = data['height']
		weight = data['weight']
		types = data['types']
		stats = data['stats']
		abilities = data['abilities']

		pokemonData = {
			'image': image,
			'abilities': abilities,
			'types': types,
			'stats': stats,
			'weight': weight,
			'height': height
		}

		return pokemonData


	def getPokemonData(self, url):
		data = self.GET(url)

		json = self.toJSON(data)

		return json



if __name__ == '__main__':
	main()