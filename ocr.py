import requests
import re
import subprocess

# API DATA
_url = 'https://southeastasia.api.cognitive.microsoft.com/vision/v1.0/ocr?language=en&detectOrientation=true'
_key = 'ed557adf841c48e3992cdf16069b8009'  #Here you have to paste your primary key
_maxNumRetries = 10

def processRequest( json, data, headers, params ):

	"""
	Helper function to process the request to Project Oxford

	Parameters:
	json: Used when processing images from its URL. See API Documentation
	data: Used when processing image read from disk. See API Documentation
	headers: Used to pass the key information and the data type request
	"""

	retries = 0
	result = None

	while True:

		response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = params )

		if response.status_code == 429: 

			print( "Message: %s" % ( response.json() ) )

			if retries <= _maxNumRetries: 
				time.sleep(1) 
				retries += 1
				continue
			else: 
				print( 'Error: failed after retrying!' )
				break

		elif response.status_code == 200 or response.status_code == 201:

			if 'content-length' in response.headers and int(response.headers['content-length']) == 0: 
				result = None 
			elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str): 
				if 'application/json' in response.headers['content-type'].lower(): 
					result = response.json() if response.content else None 
				elif 'image' in response.headers['content-type'].lower(): 
					result = response.content
		else:
			print( "Error code: %d" % ( response.status_code ) )
			print( "Message: %s" % ( response.json() ) )

		break
		
	return result

def format(words):
	words = words.upper()
	words = re.sub('^.*INGREDIENTS:','',words,1)
	words = re.sub('\)|\(|\-',', ',words)
	words = words.split(', ')
	return words

def ocr(filename): 
	# URL direction to image
	# urlImage = 'https://notesfromthefunnyfarm.files.wordpress.com/2010/06/muffin-mix-ingredients.jpg'
	# urlImage = 'http://fitzala.com/wp-content/uploads/2014/03/cereal-ingredients.jpg'
	# Computer Vision parameters
	# params = { 'visualFeatures' : 'Color,Categories'} 
	
	params={}
	headers = dict()
	headers['Ocp-Apim-Subscription-Key'] = _key
	headers['Content-Type'] = 'application/octet-stream' 

	# json = { 'url': urlImage } 
	json={}
	data = open(filename, "rb")

	result = processRequest( json, data, headers, params )
	print(result)

	bounding_boxes =[]
	words=""
	if result is not None:
		
		for r in result['regions']:
			for l in r['lines']:
				for w in l['words']:
					words+=w['text']+" "
					# bounding_boxes+= (w['text'],w['boundingBox'])

		# Bounding boxes 
		line_infos = [region["lines"] for region in result["regions"]]
		bounding_boxes = []
		for line in line_infos:
		    for word_metadata in line:
		        for word_info in word_metadata["words"]:
		            bounding_boxes.append(word_info)
		# print(bounding_boxes)

	# 	words=words.replace(':',',')
		words = format(words)
		print ("\n".join(words))
	return words,bounding_boxes