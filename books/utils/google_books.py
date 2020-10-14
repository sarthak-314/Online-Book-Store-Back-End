import requests
import json
from urllib.parse import quote

# GOOGLE_BOOKS_API_KEY = settings.GOOGLE_BOOKS_API_KEY
GOOGLE_BOOKS_API_KEY = 'AIzaSyA4bfXaTVhy9iWK7J67oI3_ptRJ-RRUrxs'

def get_book_info(qstr):
	qstr = quote(qstr)
	response = requests.get('https://www.googleapis.com/books/v1/volumes?q='+qstr+'&key='+GOOGLE_BOOKS_API_KEY)
	# author, description, price, category, image
	title, description, author, category = None, None, None, None
	if response.status_code == 200:
		book_info = json.loads(response.content.decode('utf-8'))['items'][0]['volumeInfo']
		if 'title' in book_info:
			title = book_info['title']
		if 'description' in book_info:
			description = book_info['description']
		if 'authors' in book_info:
			author = book_info['authors'][0]
		if 'categories' in book_info:
			#Fiction, AI&Code, shit dam son
			#TODO: for c in CAT : if c == some : return 
			category = book_info['categories'][0]

		return title, description, author, category

def get_book_image(title): 
	return 'some_image_url'

def get_book_title(qstr):
	qstr = quote(qstr)
	response = requests.get('https://www.googleapis.com/books/v1/volumes?q='+qstr+'&key='+GOOGLE_BOOKS_API_KEY)
	if response.status_code == 200: 
		book_info = json.loads(response.content.decode('utf-8'))['items'][0]['volumeInfo']
		if 'title' in book_info: 
			return book_info['title']

if __name__ == '__main__':
	get_book_info('thrones  ')





