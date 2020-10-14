# import oauth2
# import urllib


# GOODREADS_KEY = 'qnwpDBtk7zcpwBVXJaYxrg'
# GOODREADS_SECRET = '3H45PM4t89kZULsD2I9NAKgnVkJgQinhOQEIJO9AAPI'
# GOODREADS_URL = 'http://www.goodreads.com'

# request_token_url = GOODREADS_URL + '/oauth/request_token'
# authorize_url = GOODREADS_URL + '/oauth/authorize/' 
# access_token_url = GOODREADS_URL + '/oauth/access_token/'

# def get_autherization_link():
# 	consumer = oauth2.Consumer(key = GOODREADS_KEY,secret = GOODREADS_SECRET)
# 	client = oauth2.Client(consumer)

# 	response, content = client.request(request_token_url, 'GET')
# 	if response['status'] != '200':
# 	    raise Exception('Invalid response: %s' % response['status'])

# 	request_token = dict(urllib.parse.parse_qsl(content))
# 	oauth_token_encoded = request_token[b'oauth_token']	
# 	oauth_token = oauth_token_encoded.decode("utf-8")

# 	authorization_link = authorize_url + '?oauth_token=' + oauth_token
# 	return authorization_link

# def authorize_user():
# 	autherization_link = get_autherization_link()
# 	is_autherized = False


# def main():
# 	consumer = oauth2.Consumer(key = GOODREADS_KEY,secret = GOODREADS_SECRET)
# 	client = oauth2.Client(consumer)

# 	response, content = client.request(request_token_url, 'GET')
# 	if response['status'] != '200':
# 	    raise Exception('Invalid response: %s' % response['status'])

# 	import urllib
# 	request_token = dict(urllib.parse.parse_qsl(content))
# 	oauth_token_encoded = request_token[b'oauth_token']	
# 	oauth_token = oauth_token_encoded.decode("utf-8")

# 	authorization_link = authorize_url + '?oauth_token=' + oauth_token
# 	accepted = 'n'
# 	print(authorization_link)
# 	return 	
# 	while accepted.lower() == 'n':
# 	    # you need to access the authorize_link via a browser,
# 	    # and proceed to manually authorize the consumer
# 	    accepted = raw_input('Have you authorized me? (y/n) ')

# 	token = oauth.Token(request_token['oauth_token'],
# 	                    request_token['oauth_token_secret'])

# 	client = oauth.Client(consumer, token)
# 	response, content = client.request(access_token_url, 'POST')
# 	if response['status'] != '200':
# 	    raise Exception('Invalid response: %s' % response['status'])

# 	# access_token = dict(urlparse.parse_qsl(content))

# 	# this is the token you should save for future uses
# 	token = oauth.Token(access_token['oauth_token'],
# 	                    access_token['oauth_token_secret'])

# 	#
# 	# As an example, let's add a book to one of the user's shelves
# 	#

# 	import urllib

# 	client = oauth.Client(consumer, token)
# 	# the book is: "Generation A" by Douglas Coupland
# 	body = urllib.urlencode({'name': 'to-read', 'book_id': 6801825})
# 	headers = {'content-type': 'application/x-www-form-urlencoded'}
# 	response, content = client.request('%s/shelf/add_to_shelf.xml' % url,
# 	                                   'POST', body, headers)
# 	# check that the new resource has been created
# 	if response['status'] != '201':
# 	    raise Exception('Cannot create resource: %s' % response['status'])
# 	else:
# 	    print('Book added!')

# if __name__ == '__main__':
# 	main()

# # import oauth2 as oauth
# # import urlparse

# # url = 'http://www.goodreads.com'
# # request_token_url = '%s/oauth/request_token/' % url
# # authorize_url = '%s/oauth/authorize/' % url
# # access_token_url = '%s/oauth/access_token/' % url

# # consumer = oauth.Consumer(key='Your-GoodReads-Key',
# #                           secret='Your-GoodReads-Secret')

# # client = oauth.Client(consumer)

# # response, content = client.request(request_token_url, 'GET')
# # if response['status'] != '200':
# #     raise Exception('Invalid response: %s' % response['status'])

# # request_token = dict(urlparse.parse_qsl(content))

# # authorize_link = '%s?oauth_token=%s' % (authorize_url,
# #                                         request_token['oauth_token'])
# # print authorize_link
# # accepted = 'n'
# # while accepted.lower() == 'n':
# #     # you need to access the authorize_link via a browser,
# #     # and proceed to manually authorize the consumer
# #     accepted = raw_input('Have you authorized me? (y/n) ')

# # token = oauth.Token(request_token['oauth_token'],
# #                     request_token['oauth_token_secret'])

# # client = oauth.Client(consumer, token)
# # response, content = client.request(access_token_url, 'POST')
# # if response['status'] != '200':
# #     raise Exception('Invalid response: %s' % response['status'])

# # access_token = dict(urlparse.parse_qsl(content))

# # # this is the token you should save for future uses
# # token = oauth.Token(access_token['oauth_token'],
# #                     access_token['oauth_token_secret'])

# # #
# # # As an example, let's add a book to one of the user's shelves
# # #

# # import urllib

# # client = oauth.Client(consumer, token)
# # # the book is: "Generation A" by Douglas Coupland
# # body = urllib.urlencode({'name': 'to-read', 'book_id': 6801825})
# # headers = {'content-type': 'application/x-wwwp-form-urlencoded'}
# # response, content = client.request('%s/shelf/add_to_shelf.xml' % url,
# #                                    'POST', body, headers)
# # # check that the new resource has been created
# # if response['status'] != '201':
# #     raise Exception('Cannot create resource: %s' % response['status'])
# # else:
# #     print 'Book added!'